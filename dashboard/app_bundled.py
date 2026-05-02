# === BEGIN theme.py ===
"""Bokeh theme for the WAGA dashboard matching charleslikesdata.com.

Exports a ``portfolio_theme`` object that is applied globally inside
``app.py``'s ``servable()`` function — NOT at module import time. Applying
at import time mutates Panel's module-level config and causes cross-test
pollution. If you find yourself importing this module and immediately
setting ``pn.config.theme``, move that call into the servable function.
"""

from typing import Any

# Palette derived from charleslikesdata.com style.css. Keep in sync with
# ``static/portfolio.css``; if the portfolio palette changes, update both.
PORTFOLIO_PALETTE: dict[str, str] = {
    "text_primary": "#353535",
    "text_secondary": "#555555",
    "bg_white": "#ffffff",
    "bg_light": "#f9f9f9",
    "bg_card_highlight": "#ebf1f8",
    "border": "#353535",
    "grid": "#f0f0f0",
}

# Data palette — desaturated, editorial. Used to encode data, not decorate.
DATA_PALETTE: dict[str, str] = {
    "primary": "#353535",
    "secondary": "#a8b8c8",
    "wind": "#4a7c7e",
    "solar": "#d4a44c",
    "performance_excellent": "#4a7c5c",
    "performance_good": "#7ca087",
    "performance_fair": "#c8a472",
    "performance_poor": "#b06a5c",
    "rolling": "#888888",
    "expected_ghost": "#cccccc",
}


def build_theme_json() -> dict[str, Any]:
    """Return the Bokeh theme JSON config.

    The theme applies Poppins font, charcoal axes, subtle dashed gridlines,
    and removes the Bokeh logo and toolbar chrome.

    Returns
    -------
    dict[str, Any]
        JSON dict suitable for constructing a ``bokeh.themes.Theme``.
    """
    return {
        "attrs": {
            "figure": {
                "background_fill_color": PORTFOLIO_PALETTE["bg_white"],
                "border_fill_color": PORTFOLIO_PALETTE["bg_white"],
                "outline_line_color": None,
            },
            "Axis": {
                "axis_label_text_font": "Poppins",
                "axis_label_text_font_size": "12px",
                "axis_label_text_color": PORTFOLIO_PALETTE["text_primary"],
                "axis_label_text_font_style": "normal",
                "major_label_text_font": "Poppins",
                "major_label_text_color": PORTFOLIO_PALETTE["text_secondary"],
                "major_tick_line_color": PORTFOLIO_PALETTE["text_primary"],
                "minor_tick_line_color": None,
                "axis_line_color": PORTFOLIO_PALETTE["text_primary"],
            },
            "Grid": {
                "grid_line_color": PORTFOLIO_PALETTE["grid"],
                "grid_line_dash": [4, 4],
            },
            "Title": {
                "text_font": "Poppins",
                "text_font_size": "14px",
                "text_font_style": "normal",
                "text_color": PORTFOLIO_PALETTE["text_primary"],
            },
            "Legend": {
                "background_fill_alpha": 0.9,
                "border_line_color": None,
                "label_text_font": "Poppins",
                "label_text_color": PORTFOLIO_PALETTE["text_secondary"],
            },
            "Toolbar": {
                "logo": None,
            },
        }
    }


def load_theme() -> Any:
    """Construct the Bokeh ``Theme`` object.

    Import is lazy so tests and non-Pyodide contexts can import this
    module without requiring Bokeh to be installed.

    Returns
    -------
    bokeh.themes.Theme
        Theme object suitable for ``pn.config.theme =``.
    """
    from bokeh.themes import Theme

    return Theme(json=build_theme_json())

# === BEGIN data_loader.py ===
"""Async JSON data loaders for the Panel dashboard.

Uses ``pyodide.http.pyfetch`` in the browser and falls back to a stdlib
``urllib`` read when running outside Pyodide (e.g., local tests, local
``panel serve`` smoke runs). The fallback is intentional and kept tiny
so tests can exercise the parsing and schema handling without needing
a browser runtime.

Important: do NOT use ``requests`` here. ``requests`` relies on sockets
that the Pyodide sandbox does not expose, so the browser build would
break at import time.
"""

import json
import sys
from dataclasses import dataclass
from typing import Any

import polars as pl

# Resolved lazily so importing this module doesn't hit the network.
_CACHE: dict[str, Any] = {}

_HTTP_ERROR_FLOOR = 400

EXPECTED_SCHEMA_VERSION = "1.0"

# Relative data directory served by GitHub Pages alongside the compiled
# Panel app. Lives at ``charleslikesdata.com/dashboard/data/*.json``.
DEFAULT_DATA_BASE = "./data"


@dataclass(frozen=True)
class Manifest:
    """Dashboard export manifest metadata.

    Parsed from ``manifest.json``. ``schema_version`` is compared against
    ``EXPECTED_SCHEMA_VERSION`` at app startup; mismatch triggers a
    non-blocking warning banner in the UI.
    """

    generated_at: str
    pipeline_run_id: str
    date_range_start: str
    date_range_end: str
    asset_count: int
    row_counts: dict[str, int]
    schema_version: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Manifest":
        """Construct a ``Manifest`` from a parsed JSON dict.

        Missing optional fields default to empty values; missing required
        fields raise ``KeyError`` so the app can surface a clear error.
        """
        return cls(
            generated_at=data["generated_at"],
            pipeline_run_id=data.get("pipeline_run_id", ""),
            date_range_start=data["date_range"]["start"],
            date_range_end=data["date_range"]["end"],
            asset_count=int(data["asset_count"]),
            row_counts=dict(data.get("row_counts", {})),
            schema_version=data.get("schema_version", ""),
        )

    @property
    def schema_matches(self) -> bool:
        """Return True if the exported schema matches the app's expectation."""
        return self.schema_version == EXPECTED_SCHEMA_VERSION


def clear_cache() -> None:
    """Drop all cached payloads. Useful in tests."""
    _CACHE.clear()


async def _fetch_text(url: str) -> str:
    """Fetch a URL and return the response body as text.

    In Pyodide, uses ``pyodide.http.pyfetch`` (async). Outside Pyodide,
    falls back to ``urllib.request.urlopen`` synchronously.

    Parameters
    ----------
    url : str
        Absolute or relative URL to fetch.

    Returns
    -------
    str
        Response body.

    Raises
    ------
    RuntimeError
        If the fetch fails. The caller translates this into an error banner.
    """
    if "pyodide" in sys.modules:
        try:
            from pyodide.http import pyfetch  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError(
                "pyodide is imported but pyodide.http.pyfetch is unavailable"
            ) from exc
        response = await pyfetch(url)
        if response.status >= _HTTP_ERROR_FLOOR:
            raise RuntimeError(f"Fetch of {url} failed with HTTP {response.status}")
        return await response.string()

    # Non-Pyodide fallback (tests, local dev): synchronous urllib.
    import urllib.error
    import urllib.request

    try:
        with urllib.request.urlopen(url) as response:
            return str(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Fetch of {url} failed: {exc}") from exc


async def load_json(name: str, base: str = DEFAULT_DATA_BASE) -> Any:
    """Fetch and parse a JSON file from the dashboard data directory.

    Results are cached by ``name``; subsequent calls return the cached
    payload without a network round trip. Call ``clear_cache()`` in tests.

    Parameters
    ----------
    name : str
        File name (e.g., ``daily_performance.json``).
    base : str, optional
        Base URL/path. Defaults to ``./data`` (relative to the served
        Panel app).

    Returns
    -------
    Any
        Parsed JSON structure (list or dict).

    Raises
    ------
    RuntimeError
        If the fetch fails.
    json.JSONDecodeError
        If the response body is not valid JSON.
    """
    cache_key = f"{base}/{name}"
    if cache_key in _CACHE:
        return _CACHE[cache_key]
    payload = await _fetch_text(cache_key)
    parsed = json.loads(payload)
    _CACHE[cache_key] = parsed
    return parsed


async def load_manifest(base: str = DEFAULT_DATA_BASE) -> Manifest:
    """Load and parse ``manifest.json``."""
    raw = await load_json("manifest.json", base=base)
    return Manifest.from_dict(raw)


async def load_daily_performance(base: str = DEFAULT_DATA_BASE) -> pl.DataFrame:
    """Load ``daily_performance.json`` as a Polars DataFrame."""
    raw = await load_json("daily_performance.json", base=base)
    return pl.DataFrame(raw)


async def load_assets(base: str = DEFAULT_DATA_BASE) -> pl.DataFrame:
    """Load ``assets.json`` as a Polars DataFrame."""
    raw = await load_json("assets.json", base=base)
    return pl.DataFrame(raw)


async def load_weather_performance(base: str = DEFAULT_DATA_BASE) -> pl.DataFrame:
    """Load ``weather_performance.json`` as a Polars DataFrame."""
    raw = await load_json("weather_performance.json", base=base)
    return pl.DataFrame(raw)

# === BEGIN filters.py ===
"""Reactive filter state for the WAGA dashboard.

Exports a ``Filters`` ``param.Parameterized`` class whose params drive all
reactive dashboard components, and a pure ``filter_assets_by_type()`` helper
that is tested independently.

**Bundler note**: this file is inlined by ``scripts/build_dashboard_app.py``
before ``app.py`` is appended. Imports from ``weather_analytics.dashboard.*``
are stripped automatically. All other imports must be available inside Pyodide
or deferred inside functions.
"""

from typing import Any

import param
import polars as pl


def filter_assets_by_type(assets_df: pl.DataFrame, asset_type: str) -> list[str]:
    """Return a list of asset_id values matching *asset_type*, prefixed by 'All'.

    Parameters
    ----------
    assets_df : pl.DataFrame
        Assets table with at minimum ``asset_id`` and ``asset_type`` columns.
    asset_type : str
        One of ``"All"``, ``"Wind"``, or ``"Solar"``. When ``"All"``, every
        asset_id is returned regardless of type.

    Returns
    -------
    list[str]
        ``["All", *matching_asset_ids]``. Always starts with ``"All"`` so the
        param Selector always has a valid default.
    """
    if assets_df.is_empty():
        return ["All"]
    if asset_type == "All":
        ids = assets_df["asset_id"].to_list()
    else:
        ids = assets_df.filter(
            pl.col("asset_type").str.to_lowercase() == asset_type.lower()
        )["asset_id"].to_list()
    return ["All", *ids]


class Filters(param.Parameterized):
    """Reactive parameter container for dashboard-wide filter state.

    Params
    ------
    asset_id : str
        Currently selected asset. ``"All"`` means no asset filter applied.
    asset_type : str
        Asset-type toggle: ``"All"``, ``"Wind"``, or ``"Solar"``.
    date_start : str
        ISO-8601 date string for the start of the selected range (inclusive).
        Empty string means no lower bound.
    date_end : str
        ISO-8601 date string for the end of the selected range (inclusive).
        Empty string means no upper bound.
    """

    asset_id: Any = param.Selector(default="All", objects=["All"])
    asset_type: Any = param.Selector(default="All", objects=["All", "Wind", "Solar"])
    date_start: Any = param.String(default="")
    date_end: Any = param.String(default="")

    # Internal store so the asset_type watcher can re-filter.
    _assets_df: pl.DataFrame = param.Parameter(default=None, precedence=-1)

    def initialize(
        self, assets_df: pl.DataFrame, date_start: str, date_end: str
    ) -> None:
        """Populate filter state from loaded data.

        Call this once after awaiting the data loaders. Sets the date strings
        and populates ``asset_id.objects`` with every asset in *assets_df*.

        Parameters
        ----------
        assets_df : pl.DataFrame
            Assets table (``asset_id``, ``asset_type``, ``display_name``, …).
        date_start : str
            ISO-8601 start date from the manifest (e.g. ``"2025-01-01"``).
        date_end : str
            ISO-8601 end date from the manifest (e.g. ``"2026-04-11"``).
        """
        self._assets_df = assets_df
        self.date_start = date_start
        self.date_end = date_end
        objects = filter_assets_by_type(assets_df, "All")
        self.param["asset_id"].objects = objects
        # Keep asset_id at "All" after populating the list.
        self.asset_id = "All"

    @param.depends("asset_type", watch=True)
    def _reset_asset_id_on_type_change(self) -> None:
        """Watcher: re-filter asset objects and reset asset_id if needed."""
        assets_df = self._assets_df
        if assets_df is None:
            return
        new_objects = filter_assets_by_type(assets_df, self.asset_type)
        self.param["asset_id"].objects = new_objects
        if self.asset_id not in new_objects:
            self.asset_id = "All"

# === BEGIN kpi_cards.py ===
"""KPI card row for the WAGA dashboard.

Exports:
- ``compute_kpis()`` — pure function (fully testable without Panel)
- ``kpi_row()`` — returns a ``pn.Row`` of four reactive KPI cards

**Bundler note**: this file is inlined by ``scripts/build_dashboard_app.py``
before ``app.py`` is appended. Imports from ``weather_analytics.dashboard.*``
are stripped automatically.
"""

from typing import Any

import polars as pl

_DASH = "—"

# Card CSS applied inline so the bundled Pyodide build is self-contained.
_CARD_CSS = """
.kpi-card {
  background: #ffffff;
  border-left: 4px solid #353535;
  border-radius: 0 10px 10px 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  padding: 1.25rem 1.5rem 1.25rem 1.25rem;
  font-family: "Poppins", sans-serif;
  min-width: 180px;
  flex: 1;
}
.kpi-value {
  font-size: 2.2rem;
  font-weight: 600;
  color: #353535;
  margin: 0;
  line-height: 1.1;
}
.kpi-label {
  font-size: 0.7rem;
  font-weight: 500;
  color: #555555;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 0.5rem;
}
"""


def compute_kpis(
    daily_df: pl.DataFrame,
    weather_df: pl.DataFrame,
    asset_id: str,
    asset_type: str,
    date_start: str,
    date_end: str,
) -> dict[str, str]:
    """Compute the four dashboard KPI values from filtered DataFrames.

    All filtering happens inside this function so it is pure and fully
    testable without Panel.

    Parameters
    ----------
    daily_df : pl.DataFrame
        Daily performance data. Must contain ``asset_id``, ``asset_type``,
        ``date``, ``total_net_generation_mwh``, ``daily_capacity_factor``,
        and ``avg_availability_pct`` columns.
    weather_df : pl.DataFrame
        Weather-adjusted performance data. Must contain ``asset_id``,
        ``date``, and ``performance_score`` columns.
    asset_id : str
        Selected asset ID or ``"All"`` for no asset filter.
    asset_type : str
        ``"All"``, ``"Wind"``, or ``"Solar"``.
    date_start : str
        ISO-8601 start date (inclusive). Empty string = no lower bound.
    date_end : str
        ISO-8601 end date (inclusive). Empty string = no upper bound.

    Returns
    -------
    dict[str, str]
        Keys: ``total_mwh``, ``avg_capacity_factor``, ``avg_availability``,
        ``avg_performance_score``. Values are formatted strings or ``"—"``
        when the filtered result is empty.
    """
    d = _apply_filters(daily_df, asset_id, asset_type, date_start, date_end)
    w = _apply_filters(weather_df, asset_id, "All", date_start, date_end)

    total_mwh = _safe_sum(d, "total_net_generation_mwh")
    avg_cf = _safe_mean(d, "daily_capacity_factor", decimals=4)
    avg_avail = _safe_mean(d, "avg_availability_pct", decimals=1)
    avg_perf = _safe_mean(w, "performance_score", decimals=4)

    return {
        "total_mwh": total_mwh,
        "avg_capacity_factor": avg_cf,
        "avg_availability": avg_avail,
        "avg_performance_score": avg_perf,
    }


def _apply_filters(
    df: pl.DataFrame,
    asset_id: str,
    asset_type: str,
    date_start: str,
    date_end: str,
) -> pl.DataFrame:
    """Return *df* narrowed to rows matching all active filters."""
    result = df
    if asset_id != "All" and "asset_id" in result.columns:
        result = result.filter(pl.col("asset_id") == asset_id)
    if asset_type != "All" and "asset_type" in result.columns:
        result = result.filter(
            pl.col("asset_type").str.to_lowercase() == asset_type.lower()
        )
    if date_start and "date" in result.columns:
        result = result.filter(pl.col("date") >= date_start)
    if date_end and "date" in result.columns:
        result = result.filter(pl.col("date") <= date_end)
    return result


def _safe_sum(df: pl.DataFrame, col: str) -> str:
    """Return sum of *col* as a string, or ``"—"`` if empty."""
    if df.is_empty() or col not in df.columns:
        return _DASH
    total = df[col].sum()
    if total is None:
        return _DASH
    return str(float(total))


def _safe_mean(df: pl.DataFrame, col: str, *, decimals: int = 2) -> str:
    """Return mean of *col* rounded to *decimals* places, or ``"—"`` if empty."""
    if df.is_empty() or col not in df.columns:
        return _DASH
    mean_val = df[col].mean()
    if mean_val is None:
        return _DASH
    return f"{float(mean_val):.{decimals}f}"


def kpi_row(filters: Any) -> Any:
    """Return a ``pn.Row`` of four reactive KPI cards driven by *filters*.

    Each card re-renders whenever any filter param changes. Data is read
    from ``filters._daily_df`` and ``filters._weather_df`` which are
    populated by ``app.py`` after the loaders resolve.

    Parameters
    ----------
    filters : Filters
        Populated ``Filters`` instance (after ``initialize()`` has been
        called and ``_daily_df`` / ``_weather_df`` have been set).

    Returns
    -------
    pn.Row
        A Panel row containing four ``pn.pane.HTML`` KPI cards.
    """
    import panel as pn

    def _card(label: str, value_key: str) -> Any:
        @pn.depends(
            filters.param.asset_id,
            filters.param.asset_type,
            filters.param.date_start,
            filters.param.date_end,
        )
        def _render(
            asset_id: str,
            asset_type: str,
            date_start: str,
            date_end: str,
        ) -> pn.pane.HTML:
            _raw_daily = getattr(filters, "_daily_df", None)
            daily_df: pl.DataFrame = (
                _raw_daily if _raw_daily is not None else pl.DataFrame()
            )
            _raw_weather = getattr(filters, "_weather_df", None)
            weather_df: pl.DataFrame = (
                _raw_weather if _raw_weather is not None else pl.DataFrame()
            )
            kpis = compute_kpis(
                daily_df, weather_df, asset_id, asset_type, date_start, date_end
            )
            value = kpis[value_key]
            html = (
                f"<style>{_CARD_CSS}</style>"
                f'<div class="kpi-card">'
                f'<p class="kpi-value">{value}</p>'
                f'<p class="kpi-label">{label}</p>'
                f"</div>"
            )
            return pn.pane.HTML(html, sizing_mode="stretch_width")

        return pn.panel(_render)

    return pn.Row(
        _card("Total MWh", "total_mwh"),
        _card("Avg Capacity Factor", "avg_capacity_factor"),
        _card("Avg Availability %", "avg_availability"),
        _card("Avg Performance Score", "avg_performance_score"),
        sizing_mode="stretch_width",
    )

# === BEGIN _chart_helpers.py ===
"""Shared Bokeh figure utilities for the WAGA dashboard.

Exports:
- ``make_themed_figure`` — factory for themed, toolbar-free Bokeh figures
- ``with_empty_guard`` — renders a Markdown placeholder for empty DataFrames
- ``style_tooltip`` — attaches a HoverTool to a figure

**Bundler note**: this file is inlined by ``scripts/build_dashboard_app.py``
before ``app.py`` is appended. Imports from ``weather_analytics.dashboard.*``
are stripped automatically.
"""

from typing import Any

import polars as pl
from bokeh.plotting import figure


def make_themed_figure(
    title: str,
    x_label: str,
    y_label: str,
    **kwargs: Any,
) -> Any:
    """Create a themed Bokeh figure with no toolbar and stretch_width sizing.

    Parameters
    ----------
    title : str
        Chart title displayed above the plot.
    x_label : str
        Label for the x-axis.
    y_label : str
        Label for the y-axis.
    **kwargs : Any
        Additional keyword arguments forwarded to ``bokeh.plotting.figure``
        (e.g. ``x_axis_type="datetime"``).

    Returns
    -------
    bokeh.plotting.figure
        Configured Bokeh figure ready for glyphs.
    """
    fig = figure(
        title=title,
        x_axis_label=x_label,
        y_axis_label=y_label,
        toolbar_location=None,
        sizing_mode="stretch_width",
        **kwargs,
    )
    fig.toolbar.logo = None
    return fig


def with_empty_guard(
    df: pl.DataFrame,
    render_fn: Any,
    message: str = "No data available",
) -> Any:
    """Return a Markdown placeholder when *df* is empty, else call *render_fn*.

    Parameters
    ----------
    df : pl.DataFrame
        DataFrame to check.
    render_fn : callable
        Called with *df* when it is non-empty. Its return value is passed
        through to the caller.
    message : str, optional
        Message shown inside the Markdown pane when *df* is empty.
        Defaults to ``"No data available"``.

    Returns
    -------
    Any
        ``pn.pane.Markdown`` when *df* is empty, else ``render_fn(df)``.
    """
    import panel as pn

    if df.is_empty():
        return pn.pane.Markdown(f"_{message}_")
    return render_fn(df)


def style_tooltip(fig: Any, tooltips: list[tuple[str, str]]) -> None:
    """Attach a HoverTool with *tooltips* to *fig*.

    Parameters
    ----------
    fig : bokeh.plotting.figure
        Target Bokeh figure.
    tooltips : list[tuple[str, str]]
        Tooltip spec as ``[(label, "@column"), ...]``.

    Returns
    -------
    None
    """
    from bokeh.models import HoverTool

    hover = HoverTool(tooltips=tooltips)
    fig.add_tools(hover)

# === BEGIN fleet_view.py ===
"""Fleet Overview tab for the WAGA dashboard.

Exports:
- ``fleet_panel`` — reactive pn.Column with three charts
- Pure data-preparation functions (tested independently):
  - ``_apply_fleet_filters``
  - ``_prep_generation_lines``
  - ``_prep_capacity_bars``
  - ``_prep_heatmap``
  - ``_asset_color``

**Bundler note**: this file is inlined by ``scripts/build_dashboard_app.py``
before ``app.py`` is appended. Imports from ``weather_analytics.dashboard.*``
are stripped automatically.
"""

from datetime import datetime
from typing import Any

import polars as pl


# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

_WIND_COLOR = "#4a7c7e"
_SOLAR_COLOR = "#d4a44c"
_FALLBACK_COLOR = "#888888"

# Per-asset palette for the generation line chart — desaturated, editorial.
# Keyed by position (index) so each asset gets a distinct colour regardless
# of type; up to 8 assets before cycling.
_ASSET_LINE_PALETTE: list[str] = [
    "#353535",  # charcoal
    "#4a7c7e",  # dusty teal
    "#a87c40",  # muted amber
    "#5a6e8a",  # steel blue
    "#6b5b72",  # dusty plum
    "#5a7a5a",  # sage
    "#8a5a4a",  # terracotta
    "#7a7a7a",  # stone
]

_MAX_HEATMAP_DAYS = 90


def _asset_color(asset_type: str) -> str:
    """Return the chart color for *asset_type* (case-insensitive).

    Parameters
    ----------
    asset_type : str
        Asset type string — ``"wind"`` / ``"Wind"``, ``"solar"`` / ``"Solar"``,
        or any other string.

    Returns
    -------
    str
        Hex color string.
    """
    normalized = asset_type.strip().lower()
    if normalized == "wind":
        return _WIND_COLOR
    if normalized == "solar":
        return _SOLAR_COLOR
    return _FALLBACK_COLOR


# ---------------------------------------------------------------------------
# Pure data-preparation helpers
# ---------------------------------------------------------------------------


def _apply_fleet_filters(
    daily_df: pl.DataFrame,
    assets_df: pl.DataFrame,
    asset_id: str,
    asset_type: str,
    date_start: str,
    date_end: str,
) -> pl.DataFrame:
    """Join daily_df with assets_df and apply all four filters.

    Parameters
    ----------
    daily_df : pl.DataFrame
        Daily performance rows (``asset_id``, ``date``, …).
    assets_df : pl.DataFrame
        Assets lookup table with ``asset_id`` and ``asset_type``.
    asset_id : str
        ``"All"`` or a specific asset identifier.
    asset_type : str
        ``"All"``, ``"Wind"``, or ``"Solar"``.
    date_start : str
        ISO-8601 start date (inclusive). Empty string = no lower bound.
    date_end : str
        ISO-8601 end date (inclusive). Empty string = no upper bound.

    Returns
    -------
    pl.DataFrame
        Filtered rows with ``asset_type`` column added via left join.
    """
    # Left-join to attach asset_type for color mapping.
    result = daily_df.join(
        assets_df.select(["asset_id", "asset_type"]),
        on="asset_id",
        how="left",
    )

    if asset_id != "All":
        result = result.filter(pl.col("asset_id") == asset_id)
    if asset_type != "All":
        result = result.filter(
            pl.col("asset_type").str.to_lowercase() == asset_type.lower()
        )
    if date_start:
        result = result.filter(pl.col("date") >= date_start)
    if date_end:
        result = result.filter(pl.col("date") <= date_end)

    return result


def _prep_generation_lines(
    df: pl.DataFrame,
) -> list[tuple[str, list[datetime], list[float], str]]:
    """Build per-asset line data for the generation-over-time chart.

    Parameters
    ----------
    df : pl.DataFrame
        Filtered daily DataFrame with ``asset_id``, ``date``,
        ``total_net_generation_mwh``, and ``asset_type`` columns.

    Returns
    -------
    list[tuple[str, list[datetime], list[float], str]]
        One entry per asset: ``(asset_id, dates, values, color)`` where
        *dates* are ``datetime`` objects (midnight) for Bokeh's datetime axis.
    """
    if df.is_empty():
        return []

    lines: list[tuple[str, list[datetime], list[float], str]] = []
    sorted_asset_ids = df["asset_id"].unique(maintain_order=False).sort().to_list()
    for idx, asset_id_val in enumerate(sorted_asset_ids):
        asset_rows = df.filter(pl.col("asset_id") == asset_id_val).sort("date")
        dates: list[datetime] = [
            datetime.fromisoformat(d) for d in asset_rows["date"].to_list()
        ]
        values: list[float] = asset_rows["total_net_generation_mwh"].to_list()
        color = _ASSET_LINE_PALETTE[idx % len(_ASSET_LINE_PALETTE)]
        lines.append((asset_id_val, dates, values, color))

    return lines


def _prep_capacity_bars(
    df: pl.DataFrame,
) -> tuple[list[str], list[float], list[str]]:
    """Compute mean capacity factor per asset, sorted descending.

    Parameters
    ----------
    df : pl.DataFrame
        Filtered daily DataFrame with ``asset_id``, ``daily_capacity_factor``,
        and ``asset_type`` columns.

    Returns
    -------
    tuple[list[str], list[float], list[str]]
        ``(asset_ids, mean_cfs, colors)`` — three parallel lists.
        Sorted so the highest mean CF is first.
    """
    if df.is_empty():
        return [], [], []

    agg = (
        df.group_by(["asset_id", "asset_type"])
        .agg(pl.col("daily_capacity_factor").mean().alias("mean_cf"))
        .sort("mean_cf", descending=True)
    )

    asset_ids: list[str] = agg["asset_id"].to_list()
    mean_cfs: list[float] = agg["mean_cf"].to_list()
    colors: list[str] = [_asset_color(t) for t in agg["asset_type"].to_list()]

    return asset_ids, mean_cfs, colors


def _prep_heatmap(
    weather_df: pl.DataFrame,
    assets_df: pl.DataFrame,
    asset_id: str,
    asset_type: str,
    date_start: str,
    date_end: str,
) -> pl.DataFrame:
    """Filter weather performance data for the heatmap chart.

    Caps the date range at ``_MAX_HEATMAP_DAYS`` most recent distinct dates
    to keep the chart readable.

    Parameters
    ----------
    weather_df : pl.DataFrame
        Weather performance rows (``asset_id``, ``date``, ``performance_score``).
    assets_df : pl.DataFrame
        Assets lookup table with ``asset_id`` and ``asset_type``.
    asset_id : str
        ``"All"`` or a specific asset identifier.
    asset_type : str
        ``"All"``, ``"Wind"``, or ``"Solar"``.
    date_start : str
        ISO-8601 start date (inclusive). Empty string = no lower bound.
    date_end : str
        ISO-8601 end date (inclusive). Empty string = no upper bound.

    Returns
    -------
    pl.DataFrame
        Filtered rows with columns ``asset_id``, ``date``,
        ``performance_score``, ``asset_type``.
    """
    result = weather_df.join(
        assets_df.select(["asset_id", "asset_type"]),
        on="asset_id",
        how="left",
    )

    if asset_id != "All":
        result = result.filter(pl.col("asset_id") == asset_id)
    if asset_type != "All":
        result = result.filter(
            pl.col("asset_type").str.to_lowercase() == asset_type.lower()
        )
    if date_start:
        result = result.filter(pl.col("date") >= date_start)
    if date_end:
        result = result.filter(pl.col("date") <= date_end)

    # Cap to most recent _MAX_HEATMAP_DAYS distinct dates.
    if not result.is_empty():
        all_dates = result["date"].unique().sort(descending=True)
        if all_dates.shape[0] > _MAX_HEATMAP_DAYS:
            recent_dates = all_dates.head(_MAX_HEATMAP_DAYS)
            result = result.filter(pl.col("date").is_in(recent_dates))

    return result.select(["asset_id", "date", "performance_score", "asset_type"])


# ---------------------------------------------------------------------------
# Chart renderers
# ---------------------------------------------------------------------------


def _render_generation_chart(df: pl.DataFrame) -> Any:
    """Render the generation-over-time line chart from a filtered DataFrame."""
    import panel as pn

    lines = _prep_generation_lines(df)
    if not lines:
        return pn.pane.Markdown("_No generation data available._")

    fig = make_themed_figure(
        "Fleet Net Generation — Daily",
        "Date",
        "MWh",
        x_axis_type="datetime",
        height=350,
    )
    style_tooltip(
        fig,
        [("Date", "@x{%F}"), ("Asset", "@asset_id"), ("MWh", "@y{0.0}")],
    )
    # Update hover to format datetime
    from bokeh.models import HoverTool

    for tool in fig.tools:
        if isinstance(tool, HoverTool):
            tool.formatters = {"@x": "datetime"}

    for asset_id_val, dates, values, color in lines:
        source_data = {
            "x": dates,
            "y": values,
            "asset_id": [asset_id_val] * len(dates),
        }
        fig.line(
            x="x",
            y="y",
            source=source_data,
            line_color=color,
            line_width=2,
            legend_label=asset_id_val,
        )
        fig.scatter(
            x="x",
            y="y",
            source=source_data,
            size=6,
            fill_color=color,
            line_color=color,
            marker="circle",
        )

    fig.legend.location = "top_left"
    fig.legend.click_policy = "hide"
    return pn.pane.Bokeh(fig, sizing_mode="stretch_width")


def _render_capacity_chart(df: pl.DataFrame) -> Any:
    """Render the horizontal capacity factor bar chart."""
    import panel as pn

    asset_ids, mean_cfs, colors = _prep_capacity_bars(df)
    if not asset_ids:
        return pn.pane.Markdown("_No capacity factor data available._")

    fig = make_themed_figure(
        "Average Capacity Factor by Asset",
        "Mean Capacity Factor",
        "Asset",
        y_range=asset_ids,
        height=max(200, len(asset_ids) * 40),
    )
    style_tooltip(fig, [("Asset", "@asset_id"), ("Mean CF", "@right{0.000}")])

    source_data = {
        "asset_id": asset_ids,
        "right": mean_cfs,
        "color": colors,
    }
    fig.hbar(
        y="asset_id",
        right="right",
        height=0.6,
        fill_color="color",
        line_color="color",
        source=source_data,
    )
    return pn.pane.Bokeh(fig, sizing_mode="stretch_width")


def _render_heatmap_chart(df: pl.DataFrame) -> Any:
    """Render the performance score heatmap.

    Uses a real datetime x-axis (not categorical) so Bokeh auto-spaces tick
    labels at sensible intervals (~8 labels) without crowding.
    """
    import panel as pn
    from bokeh.models import ColorBar, DatetimeTickFormatter, LinearColorMapper, Range1d
    from bokeh.palettes import Viridis256
    from bokeh.transform import transform

    asset_ids = df["asset_id"].unique().sort().to_list()

    # Parse date strings to datetime objects (strip nanosecond precision).
    def _to_dt(s: str) -> datetime:
        return datetime.fromisoformat(s[:10])

    day_ms = 24 * 60 * 60 * 1000  # milliseconds per day

    date_strs: list[str] = df["date"].to_list()
    date_ms: list[float] = [_to_dt(s).timestamp() * 1000 for s in date_strs]

    all_dates_dt = [_to_dt(s) for s in df["date"].unique().sort().to_list()]
    x_start = min(all_dates_dt).timestamp() * 1000 - day_ms / 2
    x_end = max(all_dates_dt).timestamp() * 1000 + day_ms / 2

    mapper = LinearColorMapper(
        palette=Viridis256,
        low=float(df["performance_score"].min() or 0.0),
        high=float(df["performance_score"].max() or 1.0),
    )

    fig = make_themed_figure(
        "Performance Score Heatmap",
        "Date",
        "Asset",
        x_range=Range1d(x_start, x_end),
        y_range=asset_ids,
        x_axis_type="datetime",
        height=max(200, len(asset_ids) * 40),
    )
    style_tooltip(
        fig,
        [
            ("Asset", "@asset_id"),
            ("Date", "@date_str"),
            ("Score", "@performance_score{0.000}"),
        ],
    )

    fig.xaxis.formatter = DatetimeTickFormatter(days="%b %d", months="%b %Y")
    fig.xaxis.major_label_orientation = 0.9

    source_data = {
        "asset_id": df["asset_id"].to_list(),
        "date": date_ms,
        "date_str": [s[:10] for s in date_strs],
        "performance_score": df["performance_score"].to_list(),
    }
    fig.rect(
        x="date",
        y="asset_id",
        width=day_ms * 0.95,
        height=1,
        source=source_data,
        fill_color=transform("performance_score", mapper),
        line_color=None,
    )

    color_bar = ColorBar(color_mapper=mapper, width=8)
    fig.add_layout(color_bar, "right")

    return pn.pane.Bokeh(fig, sizing_mode="stretch_width")


# ---------------------------------------------------------------------------
# Public component
# ---------------------------------------------------------------------------


def fleet_panel(filters: Any) -> Any:
    """Build a reactive pn.Column with three Fleet Overview charts.

    All three charts re-render whenever any filter parameter changes.

    Parameters
    ----------
    filters : Filters
        Populated ``Filters`` instance with ``_daily_df``, ``_weather_df``,
        and ``_assets_df`` attributes set.

    Returns
    -------
    pn.Column
        Column containing the three reactive chart panels.
    """
    import panel as pn

    @pn.depends(
        filters.param.asset_id,
        filters.param.asset_type,
        filters.param.date_start,
        filters.param.date_end,
    )
    def _generation_chart(
        asset_id: str,
        asset_type: str,
        date_start: str,
        date_end: str,
    ) -> Any:
        _raw_daily = getattr(filters, "_daily_df", None)
        daily_df: pl.DataFrame = (
            _raw_daily if _raw_daily is not None else pl.DataFrame()
        )
        _raw_assets = getattr(filters, "_assets_df", None)
        assets_df: pl.DataFrame = (
            _raw_assets if _raw_assets is not None else pl.DataFrame()
        )
        filtered = _apply_fleet_filters(
            daily_df, assets_df, asset_id, asset_type, date_start, date_end
        )
        return with_empty_guard(
            filtered,
            _render_generation_chart,
            message="No generation data for the selected filters.",
        )

    @pn.depends(
        filters.param.asset_id,
        filters.param.asset_type,
        filters.param.date_start,
        filters.param.date_end,
    )
    def _capacity_chart(
        asset_id: str,
        asset_type: str,
        date_start: str,
        date_end: str,
    ) -> Any:
        _raw_daily = getattr(filters, "_daily_df", None)
        daily_df: pl.DataFrame = (
            _raw_daily if _raw_daily is not None else pl.DataFrame()
        )
        _raw_assets = getattr(filters, "_assets_df", None)
        assets_df: pl.DataFrame = (
            _raw_assets if _raw_assets is not None else pl.DataFrame()
        )
        filtered = _apply_fleet_filters(
            daily_df, assets_df, asset_id, asset_type, date_start, date_end
        )
        return with_empty_guard(
            filtered,
            _render_capacity_chart,
            message="No capacity factor data for the selected filters.",
        )

    @pn.depends(
        filters.param.asset_id,
        filters.param.asset_type,
        filters.param.date_start,
        filters.param.date_end,
    )
    def _heatmap_chart(
        asset_id: str,
        asset_type: str,
        date_start: str,
        date_end: str,
    ) -> Any:
        _raw_weather = getattr(filters, "_weather_df", None)
        weather_df: pl.DataFrame = (
            _raw_weather if _raw_weather is not None else pl.DataFrame()
        )
        _raw_assets = getattr(filters, "_assets_df", None)
        assets_df: pl.DataFrame = (
            _raw_assets if _raw_assets is not None else pl.DataFrame()
        )
        heatmap_df = _prep_heatmap(
            weather_df, assets_df, asset_id, asset_type, date_start, date_end
        )
        return with_empty_guard(
            heatmap_df,
            _render_heatmap_chart,
            message="No performance score data for the selected filters.",
        )

    return pn.Column(
        pn.panel(_generation_chart),
        pn.panel(_capacity_chart),
        pn.panel(_heatmap_chart),
        sizing_mode="stretch_width",
    )

# === BEGIN asset_view.py ===
"""Asset Deep-Dive tab for the WAGA dashboard.

Exports:
- ``asset_panel`` — reactive pn.Column with four charts for a single asset
- Pure data-preparation functions (tested independently):
  - ``_filter_asset_daily``
  - ``_filter_asset_weather``
  - ``_get_asset_type``
  - ``_prep_expected_vs_actual``
  - ``_prep_rolling_cf``
  - ``_prep_scatter``
  - ``_prep_stacked_hours``
  - ``_fit_regression``

**Bundler note**: this file is inlined by ``scripts/build_dashboard_app.py``
before ``app.py`` is appended. Imports from ``weather_analytics.dashboard.*``
are stripped automatically.
"""

from datetime import datetime
from typing import Any

import numpy as np
import polars as pl


# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

_WIND_COLOR = "#4a7c7e"
_SOLAR_COLOR = "#d4a44c"
_ACTUAL_COLOR = "#353535"
_EXPECTED_COLOR = "#999999"
_CF_7D_COLOR = "#4a7c7e"
_CF_30D_COLOR = "#353535"
_CF_RAW_COLOR = "#cccccc"

HOUR_COLS = ["excellent_hours", "good_hours", "fair_hours", "poor_hours"]
HOUR_COLORS = ["#2d6a4f", "#52b788", "#f4a261", "#e76f51"]

_MIN_REGRESSION_POINTS = 2


# ---------------------------------------------------------------------------
# Pure data-preparation helpers
# ---------------------------------------------------------------------------


def _filter_asset_daily(
    daily_df: pl.DataFrame,
    asset_id: str,
    date_start: str,
    date_end: str,
) -> pl.DataFrame:
    """Filter daily_df to a single asset and date range.

    Parameters
    ----------
    daily_df : pl.DataFrame
        Daily performance rows.
    asset_id : str
        Specific asset identifier (not ``"All"``).
    date_start : str
        ISO-8601 start date (inclusive). Empty string = no lower bound.
    date_end : str
        ISO-8601 end date (inclusive). Empty string = no upper bound.

    Returns
    -------
    pl.DataFrame
        Filtered and sorted rows for the given asset.
    """
    result = daily_df.filter(pl.col("asset_id") == asset_id)
    if date_start:
        result = result.filter(pl.col("date") >= date_start)
    if date_end:
        result = result.filter(pl.col("date") <= date_end)
    return result.sort("date")


def _filter_asset_weather(
    weather_df: pl.DataFrame,
    asset_id: str,
    date_start: str,
    date_end: str,
) -> pl.DataFrame:
    """Filter weather_df to a single asset and date range.

    Parameters
    ----------
    weather_df : pl.DataFrame
        Weather performance rows.
    asset_id : str
        Specific asset identifier (not ``"All"``).
    date_start : str
        ISO-8601 start date (inclusive). Empty string = no lower bound.
    date_end : str
        ISO-8601 end date (inclusive). Empty string = no upper bound.

    Returns
    -------
    pl.DataFrame
        Filtered and sorted rows for the given asset.
    """
    result = weather_df.filter(pl.col("asset_id") == asset_id)
    if date_start:
        result = result.filter(pl.col("date") >= date_start)
    if date_end:
        result = result.filter(pl.col("date") <= date_end)
    return result.sort("date")


def _get_asset_type(weather_df: pl.DataFrame) -> str:
    """Return ``inferred_asset_type`` from the first row, or empty string.

    Parameters
    ----------
    weather_df : pl.DataFrame
        Already-filtered weather performance rows for a single asset.

    Returns
    -------
    str
        Asset type string (e.g. ``"Wind"`` or ``"Solar"``), or ``""`` if
        the DataFrame is empty.
    """
    if weather_df.is_empty():
        return ""
    return str(weather_df["inferred_asset_type"][0])


def _prep_expected_vs_actual(
    weather_df: pl.DataFrame,
) -> tuple[list[datetime], list[float], list[float]]:
    """Extract dates, actual MWh, and expected MWh series from weather_df.

    Parameters
    ----------
    weather_df : pl.DataFrame
        Filtered weather performance rows (pre-sorted by date).

    Returns
    -------
    tuple[list[datetime], list[float], list[float]]
        ``(dates, actual_mwh, expected_mwh)`` — three parallel lists sorted
        by date. Dates are ``datetime`` objects (midnight) for Bokeh's
        datetime axis.
    """
    if weather_df.is_empty():
        return [], [], []

    df = weather_df.sort("date")
    dates: list[datetime] = [datetime.fromisoformat(d) for d in df["date"].to_list()]
    actual: list[float] = df["avg_actual_generation_mwh"].to_list()
    expected: list[float] = df["avg_expected_generation_mwh"].to_list()
    return dates, actual, expected


def _prep_rolling_cf(
    weather_df: pl.DataFrame,
    daily_df: pl.DataFrame,
) -> tuple[list[datetime], list[float], list[float], list[float]]:
    """Extract dates and three capacity factor series.

    Uses weather_df dates as the primary axis. Joins raw ``daily_capacity_factor``
    from daily_df on the ``date`` column.

    Parameters
    ----------
    weather_df : pl.DataFrame
        Filtered weather performance rows (pre-sorted by date).
    daily_df : pl.DataFrame
        Filtered daily performance rows for the same asset.

    Returns
    -------
    tuple[list[datetime], list[float], list[float], list[float]]
        ``(dates, cf_7d, cf_30d, raw_cf)`` — four parallel lists sorted by
        date. Dates are ``datetime`` objects.
    """
    if weather_df.is_empty():
        return [], [], [], []

    df = weather_df.sort("date")

    # Join raw CF from daily_df.
    if not daily_df.is_empty():
        daily_cf = daily_df.select(["date", "daily_capacity_factor"]).sort("date")
        df = df.join(daily_cf, on="date", how="left")
        raw_cf: list[float] = df["daily_capacity_factor"].to_list()
    else:
        raw_cf = [0.0] * df.shape[0]

    dates: list[datetime] = [datetime.fromisoformat(d) for d in df["date"].to_list()]
    cf_7d: list[float] = df["rolling_7d_avg_cf"].to_list()
    cf_30d: list[float] = df["rolling_30d_avg_cf"].to_list()
    return dates, cf_7d, cf_30d, raw_cf


def _prep_scatter(
    daily_df: pl.DataFrame,
    asset_type: str,
) -> tuple[list[float], list[float], float]:
    """Extract scatter plot data (weather var vs generation) with r-squared.

    Parameters
    ----------
    daily_df : pl.DataFrame
        Filtered daily performance rows.
    asset_type : str
        ``"Wind"`` or ``"Solar"`` — determines which weather variable to use.

    Returns
    -------
    tuple[list[float], list[float], float]
        ``(x_vals, y_vals, r_squared)`` where *x_vals* are the weather
        variable values (wind speed or GHI), *y_vals* are generation MWh,
        and *r_squared* is computed from ``numpy.polyfit`` residuals.
    """
    if daily_df.is_empty():
        return [], [], 0.0

    x_col = "avg_ghi" if asset_type.lower() == "solar" else "avg_wind_speed_mps"

    # Drop rows where the weather predictor or generation is null so that
    # numpy receives only finite floats.
    df = daily_df.sort("date").drop_nulls(subset=[x_col, "total_net_generation_mwh"])

    if df.is_empty():
        return [], [], 0.0

    x_vals: list[float] = df[x_col].to_list()
    y_vals: list[float] = df["total_net_generation_mwh"].to_list()

    if len(x_vals) < _MIN_REGRESSION_POINTS:
        return x_vals, y_vals, 0.0

    x_arr = np.array(x_vals, dtype=float)
    y_arr = np.array(y_vals, dtype=float)
    coeffs = np.polyfit(x_arr, y_arr, 1)
    y_pred = np.polyval(coeffs, x_arr)
    ss_res = float(np.sum((y_arr - y_pred) ** 2))
    ss_tot = float(np.sum((y_arr - y_arr.mean()) ** 2))
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0.0 else 0.0

    return x_vals, y_vals, max(0.0, r_squared)


def _prep_stacked_hours(daily_df: pl.DataFrame) -> pl.DataFrame:
    """Return a DataFrame with the date and four hour-category columns.

    Parameters
    ----------
    daily_df : pl.DataFrame
        Filtered daily performance rows.

    Returns
    -------
    pl.DataFrame
        Subset with columns ``date``, ``excellent_hours``, ``good_hours``,
        ``fair_hours``, ``poor_hours``, sorted by date.
    """
    cols = ["date", *HOUR_COLS]
    if daily_df.is_empty():
        return pl.DataFrame(
            {
                c: pl.Series([], dtype=pl.Utf8 if c == "date" else pl.Float64)
                for c in cols
            }
        )
    return daily_df.select(cols).sort("date")


def _fit_regression(
    x_vals: list[float],
    y_vals: list[float],
) -> tuple[list[float], list[float]]:
    """Return ``(x_line, y_line)`` for a linear regression overlay.

    Parameters
    ----------
    x_vals : list[float]
        Independent variable values.
    y_vals : list[float]
        Dependent variable values.

    Returns
    -------
    tuple[list[float], list[float]]
        ``(x_sorted, y_line)`` — x values sorted ascending with corresponding
        regression-line y values.
    """
    if len(x_vals) < _MIN_REGRESSION_POINTS:
        return x_vals, y_vals
    coeffs = np.polyfit(x_vals, y_vals, 1)
    x_sorted = sorted(x_vals)
    y_line = [float(coeffs[0] * x + coeffs[1]) for x in x_sorted]
    return x_sorted, y_line


# ---------------------------------------------------------------------------
# Chart renderers
# ---------------------------------------------------------------------------


def _render_expected_vs_actual(df: pl.DataFrame, asset_id: str) -> Any:
    """Render expected vs actual generation line chart."""
    import panel as pn

    dates, actual, expected = _prep_expected_vs_actual(df)
    if not dates:
        return pn.pane.Markdown("_No expected vs. actual data available._")

    fig = make_themed_figure(
        f"Expected vs. Actual Generation \u2014 {asset_id}",
        "Date",
        "MWh",
        x_axis_type="datetime",
        height=350,
    )
    style_tooltip(
        fig,
        [
            ("Date", "@x{%F}"),
            ("Actual MWh", "@actual{0.0}"),
            ("Expected MWh", "@expected{0.0}"),
        ],
    )
    from bokeh.models import HoverTool

    for tool in fig.tools:
        if isinstance(tool, HoverTool):
            tool.formatters = {"@x": "datetime"}

    fig.line(
        x=dates,
        y=actual,
        line_color=_ACTUAL_COLOR,
        line_width=2,
        legend_label="Actual",
    )
    fig.line(
        x=dates,
        y=expected,
        line_color=_EXPECTED_COLOR,
        line_width=2,
        line_dash="dashed",
        legend_label="Expected",
    )
    fig.legend.location = "top_left"
    return pn.pane.Bokeh(fig, sizing_mode="stretch_width")


def _render_rolling_cf(
    weather_df: pl.DataFrame,
    daily_df: pl.DataFrame,
    asset_id: str,
) -> Any:
    """Render rolling capacity factor line chart."""
    import panel as pn

    dates, cf_7d, cf_30d, raw_cf = _prep_rolling_cf(weather_df, daily_df)
    if not dates:
        return pn.pane.Markdown("_No capacity factor data available._")

    fig = make_themed_figure(
        f"Capacity Factor Trends \u2014 {asset_id}",
        "Date",
        "Capacity Factor",
        x_axis_type="datetime",
        height=350,
    )
    style_tooltip(
        fig,
        [
            ("Date", "@x{%F}"),
            ("7d CF", "@cf7{0.000}"),
            ("30d CF", "@cf30{0.000}"),
        ],
    )
    from bokeh.models import HoverTool

    for tool in fig.tools:
        if isinstance(tool, HoverTool):
            tool.formatters = {"@x": "datetime"}

    fig.line(
        x=dates,
        y=raw_cf,
        line_color=_CF_RAW_COLOR,
        line_width=1,
        legend_label="Raw CF",
    )
    fig.line(
        x=dates,
        y=cf_7d,
        line_color=_CF_7D_COLOR,
        line_width=2,
        legend_label="7d Avg CF",
    )
    fig.line(
        x=dates,
        y=cf_30d,
        line_color=_CF_30D_COLOR,
        line_width=2.5,
        legend_label="30d Avg CF",
    )
    fig.legend.location = "top_left"
    return pn.pane.Bokeh(fig, sizing_mode="stretch_width")


def _render_scatter(daily_df: pl.DataFrame, asset_type: str) -> Any:
    """Render weather variable vs generation scatter with regression line."""
    import panel as pn

    x_vals, y_vals, r2 = _prep_scatter(daily_df, asset_type)
    if not x_vals:
        return pn.pane.Markdown("_No scatter data available._")

    if asset_type.lower() == "solar":
        x_label = "GHI (W/m²)"
        color = _SOLAR_COLOR
        title = f"GHI vs. Generation (R\u00b2={r2:.3f})"
    else:
        x_label = "Wind Speed (m/s)"
        color = _WIND_COLOR
        title = f"Wind Speed vs. Generation (R\u00b2={r2:.3f})"

    fig = make_themed_figure(
        title,
        x_label,
        "MWh",
        height=350,
    )
    style_tooltip(
        fig,
        [
            (x_label, "@x{0.0}"),
            ("MWh", "@y{0.0}"),
        ],
    )

    fig.scatter(
        x=x_vals,
        y=y_vals,
        size=8,
        fill_color=color,
        line_color=color,
        alpha=0.7,
    )

    if len(x_vals) >= _MIN_REGRESSION_POINTS:
        x_line, y_line = _fit_regression(x_vals, y_vals)
        fig.line(
            x=x_line,
            y=y_line,
            line_color=_ACTUAL_COLOR,
            line_width=2,
            line_dash="dashed",
        )

    return pn.pane.Bokeh(fig, sizing_mode="stretch_width")


def _render_stacked_hours(daily_df: pl.DataFrame, asset_id: str) -> Any:
    """Render stacked bar chart of performance distribution hours."""
    import panel as pn
    from bokeh.models import ColumnDataSource

    hours_df = _prep_stacked_hours(daily_df)
    if hours_df.is_empty():
        return pn.pane.Markdown("_No performance hours data available._")

    dates: list[datetime] = [
        datetime.fromisoformat(d) for d in hours_df["date"].to_list()
    ]

    # Compute bar width: one day in milliseconds * 0.8.
    bar_width_ms = 0.8 * 24 * 60 * 60 * 1000

    source = ColumnDataSource(
        {
            "x": dates,
            "excellent_hours": hours_df["excellent_hours"].to_list(),
            "good_hours": hours_df["good_hours"].to_list(),
            "fair_hours": hours_df["fair_hours"].to_list(),
            "poor_hours": hours_df["poor_hours"].to_list(),
        }
    )

    fig = make_themed_figure(
        f"Performance Distribution \u2014 {asset_id}",
        "Date",
        "Hours",
        x_axis_type="datetime",
        height=350,
    )
    style_tooltip(
        fig,
        [
            ("Date", "@x{%F}"),
            ("Excellent", "@excellent_hours{0.0}"),
            ("Good", "@good_hours{0.0}"),
            ("Fair", "@fair_hours{0.0}"),
            ("Poor", "@poor_hours{0.0}"),
        ],
    )
    from bokeh.models import HoverTool

    for tool in fig.tools:
        if isinstance(tool, HoverTool):
            tool.formatters = {"@x": "datetime"}

    fig.vbar_stack(
        HOUR_COLS,
        x="x",
        width=bar_width_ms,
        color=HOUR_COLORS,
        source=source,
        legend_label=HOUR_COLS,
    )
    fig.legend.location = "top_left"
    fig.legend.click_policy = "hide"
    return pn.pane.Bokeh(fig, sizing_mode="stretch_width")


# ---------------------------------------------------------------------------
# Public component
# ---------------------------------------------------------------------------

_PLACEHOLDER = "_Select an asset from the filter bar to view its deep-dive metrics._"


def asset_panel(filters: Any) -> Any:
    """Build a reactive pn.Column with four Asset Deep-Dive charts.

    When ``filters.asset_id == "All"``, renders a Markdown placeholder
    asking the user to select an asset. Otherwise renders four charts:
    expected vs actual generation, rolling capacity factor, scatter plot,
    and stacked performance hours.

    All charts re-render when ``asset_id``, ``date_start``, or ``date_end``
    changes.

    Parameters
    ----------
    filters : Filters
        Populated ``Filters`` instance with ``_daily_df`` and ``_weather_df``
        attributes set.

    Returns
    -------
    pn.Column
        Column containing the reactive chart panels.
    """
    import panel as pn

    @pn.depends(
        filters.param.asset_id,
        filters.param.date_start,
        filters.param.date_end,
    )
    def _charts(
        asset_id: str,
        date_start: str,
        date_end: str,
    ) -> Any:
        if asset_id == "All":
            return pn.pane.Markdown(_PLACEHOLDER)

        _raw_daily = getattr(filters, "_daily_df", None)
        daily_df: pl.DataFrame = (
            _raw_daily if _raw_daily is not None else pl.DataFrame()
        )
        _raw_weather = getattr(filters, "_weather_df", None)
        weather_df: pl.DataFrame = (
            _raw_weather if _raw_weather is not None else pl.DataFrame()
        )

        daily_filtered = (
            _filter_asset_daily(daily_df, asset_id, date_start, date_end)
            if not daily_df.is_empty()
            else daily_df
        )
        weather_filtered = (
            _filter_asset_weather(weather_df, asset_id, date_start, date_end)
            if not weather_df.is_empty()
            else weather_df
        )

        asset_type = _get_asset_type(weather_filtered)

        chart1 = with_empty_guard(
            weather_filtered,
            lambda df: _render_expected_vs_actual(df, asset_id),
            message="No expected vs. actual data for the selected filters.",
        )
        chart2 = with_empty_guard(
            weather_filtered,
            lambda df: _render_rolling_cf(df, daily_filtered, asset_id),
            message="No capacity factor data for the selected filters.",
        )
        chart3 = with_empty_guard(
            daily_filtered,
            lambda df: _render_scatter(df, asset_type),
            message="No scatter data for the selected filters.",
        )
        chart4 = with_empty_guard(
            daily_filtered,
            lambda df: _render_stacked_hours(df, asset_id),
            message="No performance hours data for the selected filters.",
        )

        return pn.Column(chart1, chart2, chart3, chart4, sizing_mode="stretch_width")

    return pn.Column(
        pn.panel(_charts),
        sizing_mode="stretch_width",
    )

# === BEGIN weather_view.py ===
"""Weather Correlation tab for the WAGA dashboard.

Exports:
- ``weather_panel`` — reactive pn.Column with three weather correlation charts
- Pure data-preparation functions (tested independently):
  - ``_prep_r2_bars``
  - ``_prep_wind_scatter``
  - ``_prep_solar_scatter``

**Bundler note**: this file is inlined by ``scripts/build_dashboard_app.py``
before ``app.py`` is appended. Imports from ``weather_analytics.dashboard.*``
are stripped automatically.
"""

from typing import Any

import polars as pl


# ---------------------------------------------------------------------------
# Palettes
# ---------------------------------------------------------------------------

_WIND_PALETTE = ["#4a7c7e", "#5ba3a6", "#2c5f61", "#7bc4c7", "#1a3d3f"]
_SOLAR_PALETTE = ["#d4a44c", "#e8c17a", "#b8892f", "#f0d9a0", "#8a6420"]

_WIND_R2_COLOR = "#4a7c7e"
_SOLAR_R2_COLOR = "#d4a44c"


# ---------------------------------------------------------------------------
# Pure data-preparation helpers
# ---------------------------------------------------------------------------


def _prep_r2_bars(
    weather_df: pl.DataFrame,
    assets_df: pl.DataFrame,
    asset_id: str,
    asset_type: str,
    date_start: str,
    date_end: str,
) -> pl.DataFrame:
    """Aggregate wind_r_squared and solar_r_squared per asset from weather_df.

    Parameters
    ----------
    weather_df : pl.DataFrame
        Weather performance rows (asset_id, date, wind_r_squared,
        solar_r_squared, inferred_asset_type).
    assets_df : pl.DataFrame
        Asset metadata with asset_id and asset_type columns.
    asset_id : str
        If not ``"All"``, filter to this specific asset.
    asset_type : str
        If not ``"All"``, filter to assets of this type via assets_df join.
    date_start : str
        ISO-8601 start date (inclusive). Empty string = no lower bound.
    date_end : str
        ISO-8601 end date (inclusive). Empty string = no upper bound.

    Returns
    -------
    pl.DataFrame
        One row per asset with columns: ``asset_id``, ``mean_wind_r2``,
        ``mean_solar_r2``. Empty if weather_df is empty.
    """
    _empty = pl.DataFrame(
        {
            "asset_id": pl.Series([], dtype=pl.Utf8),
            "mean_wind_r2": pl.Series([], dtype=pl.Float64),
            "mean_solar_r2": pl.Series([], dtype=pl.Float64),
        }
    )

    if weather_df.is_empty():
        return _empty

    df = weather_df
    if date_start:
        df = df.filter(pl.col("date") >= date_start)
    if date_end:
        df = df.filter(pl.col("date") <= date_end)

    if asset_id != "All":
        df = df.filter(pl.col("asset_id") == asset_id)

    if asset_type != "All" and not assets_df.is_empty():
        valid_ids = assets_df.filter(
            pl.col("asset_type").str.to_lowercase() == asset_type.lower()
        )["asset_id"]
        df = df.filter(pl.col("asset_id").is_in(valid_ids))

    if df.is_empty():
        return _empty

    result = df.group_by("asset_id").agg(
        pl.col("wind_r_squared").mean().alias("mean_wind_r2"),
        pl.col("solar_r_squared").mean().alias("mean_solar_r2"),
    )
    return result.sort("asset_id")


def _prep_wind_scatter(
    daily_df: pl.DataFrame,
    assets_df: pl.DataFrame,
    asset_id: str,
    date_start: str,
    date_end: str,
) -> pl.DataFrame:
    """Filter daily_df to wind assets for the wind speed vs generation scatter.

    Parameters
    ----------
    daily_df : pl.DataFrame
        Daily performance rows (asset_id, date, avg_wind_speed_mps,
        total_net_generation_mwh, ...).
    assets_df : pl.DataFrame
        Asset metadata with asset_id and asset_type columns.
    asset_id : str
        If not ``"All"``, filter to this specific asset (must be a wind asset
        for any rows to be returned).
    date_start : str
        ISO-8601 start date (inclusive). Empty string = no lower bound.
    date_end : str
        ISO-8601 end date (inclusive). Empty string = no upper bound.

    Returns
    -------
    pl.DataFrame
        Rows for wind assets with columns: ``asset_id``, ``date``,
        ``avg_wind_speed_mps``, ``total_net_generation_mwh``.
    """
    _empty = pl.DataFrame(
        {
            "asset_id": pl.Series([], dtype=pl.Utf8),
            "date": pl.Series([], dtype=pl.Utf8),
            "avg_wind_speed_mps": pl.Series([], dtype=pl.Float64),
            "total_net_generation_mwh": pl.Series([], dtype=pl.Float64),
        }
    )

    if daily_df.is_empty():
        return _empty

    wind_ids: list[str] = []
    if not assets_df.is_empty():
        wind_ids = assets_df.filter(pl.col("asset_type").str.to_lowercase() == "wind")[
            "asset_id"
        ].to_list()

    if not wind_ids:
        return _empty

    df = daily_df.filter(pl.col("asset_id").is_in(wind_ids))

    if asset_id != "All":
        df = df.filter(pl.col("asset_id") == asset_id)

    if date_start:
        df = df.filter(pl.col("date") >= date_start)
    if date_end:
        df = df.filter(pl.col("date") <= date_end)

    if df.is_empty():
        return _empty

    return df.select(
        ["asset_id", "date", "avg_wind_speed_mps", "total_net_generation_mwh"]
    ).sort(["asset_id", "date"])


def _prep_solar_scatter(
    daily_df: pl.DataFrame,
    assets_df: pl.DataFrame,
    asset_id: str,
    date_start: str,
    date_end: str,
) -> pl.DataFrame:
    """Filter daily_df to solar assets for the GHI vs generation scatter.

    Parameters
    ----------
    daily_df : pl.DataFrame
        Daily performance rows (asset_id, date, avg_ghi,
        total_net_generation_mwh, ...).
    assets_df : pl.DataFrame
        Asset metadata with asset_id and asset_type columns.
    asset_id : str
        If not ``"All"``, filter to this specific asset (must be a solar asset
        for any rows to be returned).
    date_start : str
        ISO-8601 start date (inclusive). Empty string = no lower bound.
    date_end : str
        ISO-8601 end date (inclusive). Empty string = no upper bound.

    Returns
    -------
    pl.DataFrame
        Rows for solar assets with columns: ``asset_id``, ``date``,
        ``avg_ghi``, ``total_net_generation_mwh``.
    """
    _empty = pl.DataFrame(
        {
            "asset_id": pl.Series([], dtype=pl.Utf8),
            "date": pl.Series([], dtype=pl.Utf8),
            "avg_ghi": pl.Series([], dtype=pl.Float64),
            "total_net_generation_mwh": pl.Series([], dtype=pl.Float64),
        }
    )

    if daily_df.is_empty():
        return _empty

    solar_ids: list[str] = []
    if not assets_df.is_empty():
        solar_ids = assets_df.filter(
            pl.col("asset_type").str.to_lowercase() == "solar"
        )["asset_id"].to_list()

    if not solar_ids:
        return _empty

    df = daily_df.filter(pl.col("asset_id").is_in(solar_ids))

    if asset_id != "All":
        df = df.filter(pl.col("asset_id") == asset_id)

    if date_start:
        df = df.filter(pl.col("date") >= date_start)
    if date_end:
        df = df.filter(pl.col("date") <= date_end)

    if df.is_empty():
        return _empty

    return df.select(["asset_id", "date", "avg_ghi", "total_net_generation_mwh"]).sort(
        ["asset_id", "date"]
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _color_for_index(palette: list[str], i: int) -> str:
    """Return palette[i % len(palette)].

    Parameters
    ----------
    palette : list[str]
        List of hex color strings.
    i : int
        Index into the palette (wraps around).

    Returns
    -------
    str
        Hex color string.
    """
    return palette[i % len(palette)]


# ---------------------------------------------------------------------------
# Chart renderers
# ---------------------------------------------------------------------------


def _render_r2_bars(df: pl.DataFrame) -> Any:
    """Render grouped bar chart of wind/solar R² by asset.

    Parameters
    ----------
    df : pl.DataFrame
        Result of ``_prep_r2_bars`` — one row per asset with
        ``mean_wind_r2`` and ``mean_solar_r2`` columns.

    Returns
    -------
    pn.pane.Bokeh or pn.pane.Markdown
        Bokeh pane for non-empty data, Markdown placeholder otherwise.
    """
    import panel as pn
    from bokeh.models import ColumnDataSource, FactorRange, Legend, LegendItem

    if df.is_empty():
        return pn.pane.Markdown("_No R\u00b2 data available for the current filters._")

    asset_ids: list[str] = df["asset_id"].to_list()
    wind_r2: list[float] = df["mean_wind_r2"].to_list()
    solar_r2: list[float] = df["mean_solar_r2"].to_list()

    x_wind = [(a, "Wind R\u00b2") for a in asset_ids]
    x_solar = [(a, "Solar R\u00b2") for a in asset_ids]
    x_all = x_wind + x_solar
    y_all = wind_r2 + solar_r2
    colors = [_WIND_R2_COLOR] * len(asset_ids) + [_SOLAR_R2_COLOR] * len(asset_ids)

    source = ColumnDataSource({"x": x_all, "y": y_all, "color": colors})

    fig = make_themed_figure(
        "Weather Correlation (R\u00b2) by Asset",
        "Asset",
        "R\u00b2",
        x_range=FactorRange(*x_all),
        height=350,
    )
    style_tooltip(fig, [("Asset", "@x"), ("R\u00b2", "@y{0.000}")])

    wind_bars = fig.vbar(
        x="x",
        top="y",
        width=0.4,
        color="color",
        source=source,
    )

    legend = Legend(
        items=[
            LegendItem(label="Wind R\u00b2", renderers=[wind_bars], index=0),
            LegendItem(
                label="Solar R\u00b2", renderers=[wind_bars], index=len(asset_ids)
            ),
        ]
    )
    fig.add_layout(legend, "right")
    fig.xaxis.major_label_orientation = 0.8

    return pn.pane.Bokeh(fig, sizing_mode="stretch_width")


def _render_wind_scatter(df: pl.DataFrame) -> Any:
    """Render wind speed vs generation scatter, coloured by asset.

    Parameters
    ----------
    df : pl.DataFrame
        Result of ``_prep_wind_scatter``.

    Returns
    -------
    pn.pane.Bokeh or pn.pane.Markdown
    """
    import panel as pn

    if df.is_empty():
        return pn.pane.Markdown(
            "_No wind asset data available for the current filters._"
        )

    fig = make_themed_figure(
        "Wind Speed vs. Generation (Wind Assets)",
        "Wind Speed (m/s)",
        "Net Generation (MWh)",
        height=350,
    )
    style_tooltip(
        fig,
        [
            ("Asset", "@asset_id"),
            ("Wind Speed (m/s)", "@x{0.00}"),
            ("MWh", "@y{0.0}"),
        ],
    )

    asset_ids_sorted = sorted(df["asset_id"].unique().to_list())
    for i, aid in enumerate(asset_ids_sorted):
        rows = df.filter(pl.col("asset_id") == aid)
        color = _color_for_index(_WIND_PALETTE, i)
        from bokeh.models import ColumnDataSource

        src = ColumnDataSource(
            {
                "x": rows["avg_wind_speed_mps"].to_list(),
                "y": rows["total_net_generation_mwh"].to_list(),
                "asset_id": [aid] * rows.shape[0],
            }
        )
        fig.scatter(
            x="x",
            y="y",
            source=src,
            fill_color=color,
            line_color=color,
            size=7,
            marker="circle",
            legend_label=aid,
        )

    fig.legend.location = "top_left"
    return pn.pane.Bokeh(fig, sizing_mode="stretch_width")


def _render_solar_scatter(df: pl.DataFrame) -> Any:
    """Render GHI vs generation scatter, coloured by asset.

    Parameters
    ----------
    df : pl.DataFrame
        Result of ``_prep_solar_scatter``.

    Returns
    -------
    pn.pane.Bokeh or pn.pane.Markdown
    """
    import panel as pn

    if df.is_empty():
        return pn.pane.Markdown(
            "_No solar asset data available for the current filters._"
        )

    fig = make_themed_figure(
        "GHI vs. Generation (Solar Assets)",
        "GHI (W/m\u00b2)",
        "Net Generation (MWh)",
        height=350,
    )
    style_tooltip(
        fig,
        [
            ("Asset", "@asset_id"),
            ("GHI (W/m\u00b2)", "@x{0.00}"),
            ("MWh", "@y{0.0}"),
        ],
    )

    asset_ids_sorted = sorted(df["asset_id"].unique().to_list())
    for i, aid in enumerate(asset_ids_sorted):
        rows = df.filter(pl.col("asset_id") == aid)
        color = _color_for_index(_SOLAR_PALETTE, i)
        from bokeh.models import ColumnDataSource

        src = ColumnDataSource(
            {
                "x": rows["avg_ghi"].to_list(),
                "y": rows["total_net_generation_mwh"].to_list(),
                "asset_id": [aid] * rows.shape[0],
            }
        )
        fig.scatter(
            x="x",
            y="y",
            source=src,
            fill_color=color,
            line_color=color,
            size=7,
            marker="circle",
            legend_label=aid,
        )

    fig.legend.location = "top_left"
    return pn.pane.Bokeh(fig, sizing_mode="stretch_width")


# ---------------------------------------------------------------------------
# Public component
# ---------------------------------------------------------------------------


def weather_panel(filters: Any) -> Any:
    """Build a reactive pn.Column with three weather correlation charts.

    Charts re-render when ``asset_id``, ``asset_type``, ``date_start``, or
    ``date_end`` changes on *filters*.

    The three charts are:
    1. Grouped bar: wind R² and solar R² per asset.
    2. Scatter: wind speed vs. net generation (wind assets only).
    3. Scatter: GHI vs. net generation (solar assets only).

    Parameters
    ----------
    filters : Filters
        Populated ``Filters`` instance with ``_daily_df``, ``_weather_df``,
        and ``_assets_df`` attributes set.

    Returns
    -------
    pn.Column
        Column containing the reactive chart panels.
    """
    import panel as pn

    @pn.depends(
        filters.param.asset_id,
        filters.param.asset_type,
        filters.param.date_start,
        filters.param.date_end,
    )
    def _charts(
        asset_id: str,
        asset_type: str,
        date_start: str,
        date_end: str,
    ) -> Any:
        _raw_daily = getattr(filters, "_daily_df", None)
        daily_df: pl.DataFrame = (
            _raw_daily if _raw_daily is not None else pl.DataFrame()
        )
        _raw_weather = getattr(filters, "_weather_df", None)
        weather_df: pl.DataFrame = (
            _raw_weather if _raw_weather is not None else pl.DataFrame()
        )
        _raw_assets = getattr(filters, "_assets_df", None)
        assets_df: pl.DataFrame = (
            _raw_assets if _raw_assets is not None else pl.DataFrame()
        )

        r2_df = _prep_r2_bars(
            weather_df, assets_df, asset_id, asset_type, date_start, date_end
        )
        wind_df = _prep_wind_scatter(
            daily_df, assets_df, asset_id, date_start, date_end
        )
        solar_df = _prep_solar_scatter(
            daily_df, assets_df, asset_id, date_start, date_end
        )

        chart1 = with_empty_guard(
            r2_df,
            _render_r2_bars,
            message="No R\u00b2 data for the selected filters.",
        )
        chart2 = with_empty_guard(
            wind_df,
            _render_wind_scatter,
            message="No wind asset data for the selected filters.",
        )
        chart3 = with_empty_guard(
            solar_df,
            _render_solar_scatter,
            message="No solar asset data for the selected filters.",
        )

        return pn.Column(chart1, chart2, chart3, sizing_mode="stretch_width")

    return pn.Column(
        pn.panel(_charts),
        sizing_mode="stretch_width",
    )

# === BEGIN app.py ===
"""WAGA dashboard Panel app — Phase 3.

Renders the dashboard chrome: a filter bar (asset selector, type toggle,
date range) and a KPI row (Total MWh, Avg Capacity Factor, Avg Availability,
Avg Performance Score) above an (initially empty) tab container.

**Bundler-aware imports.**
``panel convert --to pyodide-worker`` runs this file as a standalone
script inside Pyodide, not as part of the ``weather_analytics`` package.
The build script (``scripts/build_dashboard_app.py``) concatenates
``theme.py``, ``data_loader.py``, ``components/filters.py``, and
``components/kpi_cards.py`` ahead of this file and strips all
``from weather_analytics.dashboard.*`` import lines, so the symbols
are already in scope when Pyodide executes the bundle.

Do not remove these imports without also updating ``build_dashboard_app.py``
and the module list in ``MODULES_TO_INLINE``.

Notes
-----
- Panel and Bokeh are imported at module top so ``panel convert`` can
  detect the top-level ``.servable()`` call without indirection.
- Data is fetched asynchronously via ``pyodide.http.pyfetch`` in the
  browser, falling back to ``urllib`` for local ``panel serve`` runs.
- Fetch failures render a banner instead of crashing.
- Schema version mismatches render a non-blocking warning banner.
- ``console.error`` is emitted for every browser-visible error so
  operators can see them in the browser DevTools console.
"""

import sys
from datetime import datetime
from typing import Any

import panel as pn
from bokeh.io import curdoc
from bokeh.themes import Theme


_DASHBOARD_TITLE = "Weather-Adjusted Generation Analytics"
_DASHBOARD_SUBTITLE = (
    "Renewable asset performance with weather-adjusted correlations — Phase 3."
)

# Keep in sync with ``weather_analytics.dashboard.theme.DATA_PALETTE``.
_DATA_PRIMARY = "#353535"

# Inlined portfolio CSS so ``panel convert`` produces a self-contained
# bundle. Keep this in sync with
# ``weather_analytics.dashboard.static.portfolio.css``; the full CSS file
# remains the source of truth for Phase 3+ components and for local
# development via ``panel serve``.
_PORTFOLIO_CSS = """
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap");

:root {
  --color-text-primary: #353535;
  --color-text-secondary: rgb(85, 85, 85);
  --color-bg-white: #fff;
  --color-bg-light: #f9f9f9;
  --color-border: rgb(53, 53, 53);
  --color-shadow: rgba(0, 0, 0, 0.1);
}

body,
.bk-root,
.bk,
.pn-material {
  font-family: "Poppins", -apple-system, BlinkMacSystemFont, sans-serif !important;
  color: var(--color-text-primary);
  background: var(--color-bg-white);
}

h1, h2, h3, h4 {
  font-family: "Poppins", sans-serif !important;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: -0.01em;
}

h1 {
  font-size: 1.75rem;
  margin-top: 0;
}

p {
  color: var(--color-text-secondary);
  line-height: 1.6;
}

.filter-bar {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
  padding: 0.75rem 0;
}

.filter-bar select,
.filter-bar input {
  border-radius: 2rem;
  border: 1px solid var(--color-border);
  padding: 0.4rem 1rem;
  font-family: "Poppins", sans-serif;
  font-size: 0.875rem;
}
"""


def _console_error(message: str) -> None:
    """Emit ``console.error`` in the browser (no-op outside Pyodide)."""
    if "pyodide" in sys.modules:
        try:
            from js import console  # type: ignore[import-not-found]

            console.error(message)
        except ImportError:
            pass


def _error_banner(message: str) -> pn.pane.Alert:
    """Return a Panel pane rendering a warning banner."""
    return pn.pane.Alert(message, alert_type="warning")


def _schema_mismatch_banner(actual_version: str) -> pn.pane.Alert:
    """Return a banner for schema version mismatches (non-blocking)."""
    message = (
        f"Data schema version `{actual_version}` does not match "
        f"expected `{EXPECTED_SCHEMA_VERSION}`. The display may "
        f"be incorrect."
    )
    return pn.pane.Alert(message, alert_type="warning")


def _parse_iso_date(value: str) -> datetime | None:
    """Parse an ISO-8601 date string into a midnight ``datetime``.

    Returns ``None`` on failure so the caller can skip bad rows.

    Why ``datetime`` and not ``date``: Bokeh's datetime axis expects
    ``datetime.datetime`` values (which it converts to milliseconds
    since epoch). Plain ``datetime.date`` values trigger Bokeh's
    "could not set initial ranges" warning and the plot renders blank
    under its title.
    """
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _render_tracer_chart(rows: list[dict[str, Any]]) -> Any:
    """Render the tracer chart: fleet total generation over time.

    x-axis values are ``datetime`` (not ``date`` or ``str``) so Bokeh's
    datetime axis can auto-compute the data range.
    """
    from bokeh.plotting import figure

    if not rows:
        return pn.pane.Markdown("_No data available for the current range._")

    totals: dict[datetime, float] = {}
    for row in rows:
        parsed = _parse_iso_date(str(row.get("date", "")))
        if parsed is None:
            continue
        val = row.get("total_net_generation_mwh")
        if val is None:
            continue
        totals[parsed] = totals.get(parsed, 0.0) + float(val)

    if not totals:
        return pn.pane.Markdown("_No generation values found in payload._")

    sorted_dates = sorted(totals.keys())
    sorted_values = [totals[d] for d in sorted_dates]

    fig = figure(
        title="Fleet Total Net Generation — Daily",
        x_axis_label="Date",
        y_axis_label="MWh",
        x_axis_type="datetime",
        width=900,
        height=400,
    )
    fig.line(
        x=sorted_dates,
        y=sorted_values,
        line_color=_DATA_PRIMARY,
        line_width=2,
    )
    fig.scatter(
        x=sorted_dates,
        y=sorted_values,
        size=8,
        fill_color=_DATA_PRIMARY,
        line_color=_DATA_PRIMARY,
    )
    return pn.pane.Bokeh(fig)


def _build_filter_bar(filters: Filters) -> pn.Row:
    """Construct the filter bar widget row from the *filters* param object.

    Parameters
    ----------
    filters : Filters
        Populated ``Filters`` instance (after ``initialize()`` has been called).

    Returns
    -------
    pn.Row
        A Panel row containing the asset-type toggle, asset selector, and
        date-range pickers.
    """
    type_widget = pn.widgets.Select.from_param(
        filters.param.asset_type,
        name="Asset Type",
        width=140,
    )
    asset_widget = pn.widgets.Select.from_param(
        filters.param.asset_id,
        name="Asset",
        width=260,
    )
    start_widget = pn.widgets.TextInput.from_param(
        filters.param.date_start,
        name="From",
        width=140,
        placeholder="YYYY-MM-DD",
    )
    end_widget = pn.widgets.TextInput.from_param(
        filters.param.date_end,
        name="To",
        width=140,
        placeholder="YYYY-MM-DD",
    )
    return pn.Row(
        type_widget,
        asset_widget,
        start_widget,
        end_widget,
        sizing_mode="stretch_width",
        css_classes=["filter-bar"],
    )


# ---------------------------------------------------------------------------
# Shared Filters instance — created before build_body so it is accessible
# from top-level kpi_row() and the filter bar widget.
# ---------------------------------------------------------------------------
_filters = Filters()


async def build_body() -> pn.Column:
    """Fetch data, initialise filters, and build the dashboard body."""
    banners: list[Any] = []

    try:
        manifest = await load_manifest()
    except Exception as exc:
        _console_error(f"Failed to load manifest: {exc}")
        return pn.Column(
            _error_banner(
                "Data temporarily unavailable. Last successful refresh: "
                "never. Check back shortly."
            ),
            sizing_mode="stretch_width",
        )

    if not manifest.schema_matches:
        _console_error(
            f"Schema mismatch: got {manifest.schema_version}, "
            f"expected {EXPECTED_SCHEMA_VERSION}"
        )
        banners.append(_schema_mismatch_banner(manifest.schema_version))

    try:
        assets_df = await load_assets()
        daily_df = await load_daily_performance()
        weather_df = await load_weather_performance()
    except Exception as exc:
        _console_error(f"Failed to load dashboard data: {exc}")
        return pn.Column(
            _error_banner(
                "Data temporarily unavailable. Refresh failed while "
                "loading dashboard data."
            ),
            sizing_mode="stretch_width",
        )

    # Populate filter state from loaded data.
    _filters.initialize(assets_df, manifest.date_range_start, manifest.date_range_end)

    # Enrich daily and weather DataFrames with asset_type so every component
    # can filter by type without needing a separate assets join.
    asset_type_map = assets_df.select(["asset_id", "asset_type"])
    daily_df = daily_df.join(asset_type_map, on="asset_id", how="left")
    weather_df = weather_df.join(asset_type_map, on="asset_id", how="left")

    # Attach DataFrames so reactive closures can read them.
    _filters._daily_df = daily_df  # type: ignore[attr-defined]
    _filters._weather_df = weather_df  # type: ignore[attr-defined]
    _filters._assets_df = assets_df  # type: ignore[attr-defined]

    filter_bar = _build_filter_bar(_filters)
    kpi = kpi_row(_filters)

    tabs = pn.Tabs(
        ("Fleet Overview", fleet_panel(_filters)),
        ("Asset Deep-Dive", asset_panel(_filters)),
        ("Weather Correlation", weather_panel(_filters)),
        sizing_mode="stretch_width",
    )

    return pn.Column(
        *banners,
        filter_bar,
        kpi,
        tabs,
        sizing_mode="stretch_width",
    )


# ---------------------------------------------------------------------------
# Top-level Panel app assembly
#
# ``panel convert`` and ``panel serve`` both execute this file as a script
# and look for a top-level ``.servable()`` call. That call must happen at
# module top level — putting it inside a function that no one calls will
# leave the Bokeh document empty and fail the build with
# "file does not publish any Panel contents".
# ---------------------------------------------------------------------------

pn.extension(sizing_mode="stretch_width", raw_css=[_PORTFOLIO_CSS])
# Apply the Bokeh theme to the current document so every figure in this
# app picks it up.
curdoc().theme = Theme(json=build_theme_json())

_header = pn.pane.Markdown(f"# {_DASHBOARD_TITLE}\n\n{_DASHBOARD_SUBTITLE}")

# _layout is the mutable top-level column.  pn.state.onload appends the
# async body after the initial render is committed to the client, which is
# the correct pattern for pyodide-worker mode.  pn.bind(async_fn) is NOT
# used here because pyodide-worker serialises the document before async
# callbacks complete, so the body would always render blank.
_layout = pn.Column(_header, sizing_mode="stretch_width")


async def _init() -> None:
    """Fetch data and append the dashboard body to the top-level layout."""
    try:
        body = await build_body()
        _layout.append(body)
    except Exception as exc:
        _console_error(f"Dashboard initialisation failed: {exc!r}")
        _layout.append(_error_banner(f"Dashboard initialisation failed: {exc}"))


pn.state.onload(_init)
_layout.servable()

