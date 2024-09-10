/* eslint-disable no-use-before-define */
/* global $, ENV, asu_ga */

// TEST-BETA-PROD ONLY- Do not copy to DEV
const auSubAccountIds = [184, 186, 187, 188, 189, 190, 191, 192, 193, 194];
// END TEST-BETA-PROD ONLY

// PROD ONLY - Do not copy to DEV, TEST, BETA
// GA snippet
function asuGA(i, s, o, g, r, a, m) {
  // eslint-disable-next-line no-param-reassign
  i.GoogleAnalyticsObject = r;
  // eslint-disable-next-line no-param-reassign, no-unused-expressions
  (i[r] =
    i[r] ||
    // eslint-disable-next-line func-names
    function () {
      // eslint-disable-next-line prefer-rest-params, no-param-reassign
      (i[r].q = i[r].q || []).push(arguments);
      // eslint-disable-next-line no-sequences
    }),
    // eslint-disable-next-line no-param-reassign
    (i[r].l = 1 * new Date());
  // eslint-disable-next-line no-unused-expressions, prefer-destructuring, no-sequences, no-param-reassign
  (a = s.createElement(o)), (m = s.getElementsByTagName(o)[0]);
  // eslint-disable-next-line no-param-reassign
  a.async = 1;
  // eslint-disable-next-line no-param-reassign
  a.src = g;
  m.parentNode.insertBefore(a, m);
}

// <!-- Google Tag Manager -->
((w, d, s, l, i) => {
  // eslint-disable-next-line no-param-reassign
  w[l] = w[l] || [];
  w[l].push({
    'gtm.start': new Date().getTime(),
    event: 'gtm.js',
  });
  const f = d.getElementsByTagName(s)[0];
  const j = d.createElement(s);
  const dl = l !== 'dataLayer' ? `&l=${l}` : '';
  j.async = true;
  j.src = `https://www.googletagmanager.com/gtm.js?id=${i}${dl}`;
  f.parentNode.insertBefore(j, f);
})(window, document, 'script', 'dataLayer', 'GTM-PQVJ7SL');
// <!-- End Google Tag Manager -->

window.ALLY_CFG = {
  baseUrl: 'https://prod.ally.ac',
  clientId: 5430,
};

// eslint-disable-next-line no-undef
$.getScript(`${ALLY_CFG.baseUrl}/integration/canvas/ally.js`);
// END PROD ONLY - Do not copy to DEV, TEST, BETA

let asuInactiveHidden;

function setCookie(cName, cValue, expireInDays) {
  const d = new Date();
  d.setTime(d.getTime() + expireInDays * 24 * 60 * 60 * 1000);
  const expires = `expires=${d.toUTCString()}`;
  document.cookie = `${cName}=${cValue};${expires}; path=/`;
}

function getCookie(cName) {
  const name = `${cName}=`;
  const ca = document.cookie.split(';');
  let i;
  let c;
  for (i = 0; i < ca.length; i++) {
    c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return '';
}

function asuParseUrlForIdUrlSearchTerm(targetUrl, searchTerm) {
  let start;
  let end;
  if (targetUrl.indexOf(searchTerm) !== -1) {
    start = targetUrl.indexOf(searchTerm) + searchTerm.length + 1;
    end = targetUrl.indexOf('/', start + 1);
    if (end === -1) {
      // If there is no next slash, the object's Id goes to the end of the string
      end = targetUrl.length;
    }
    return targetUrl.substring(start, end);
  }
  return null;
}

// Usage: first time paginateAPI( url, processCallback, endingCallback )
// second time paginateAPI( "", processCallback, endingCallback, count, requestObject )
function paginateAPI(
  targetURL = '',
  processCallback,
  endingCallback = '',
  count = 0,
  requestObject
) {
  if (targetURL !== '') {
    $.ajax({
      url: targetURL,
      type: 'GET',
    }).done((data, status, request) => {
      const newCount = data.length;
      processCallback(data, newCount);
      paginateAPI('', processCallback, endingCallback, data.length, request);
    });
  } else if (requestObject.getResponseHeader('link').indexOf('next') > 0) {
    const linkArray = requestObject.getResponseHeader('link').split(',');
    linkArray.forEach((link) => {
      if (link.indexOf('next') > 0) {
        const nextUrl = link.substring(
          link.indexOf('<') + 1,
          link.indexOf('>')
        );
        $.ajax({
          url: nextUrl,
          type: 'GET',
        }).done((data, status, innerRequest) => {
          const newCount = count + data.length;
          processCallback(data, newCount);
          paginateAPI(
            '',
            processCallback,
            endingCallback,
            newCount,
            innerRequest
          );
        });
      }
    });
  } else if (endingCallback !== '') {
    endingCallback(count);
  }
}

// The following code can be used to identify when user content has finished loading into Canvas.
// Similar code is used as part of USU design tools (designtools.usu.edu) hence the 2 at the end of the functions
// You are free to use this however you would like - Kenneth Larsen, Utah State University
// If any of these elements exist, we will watch for page content in them to load
const klContentWrappersArray2 = [
  '#course_home_content', // Course Front Page
  '#wiki_page_show', // Content page
  '#discussion_topic', // Discussions page
  '#course_syllabus', // Syllabus page
  '#assignment_show', // Assignments page
  '#wiki_page_revisions',
  '#people-options', // People page
  '#gradebook_wrapper', // Gradebook (instructor)
];

// Check to see if the page content has loaded yet
function klPageContentCheck2(klContentWrapperElement2, checkCount) {
  let contentLoaded = false;
  // Content Pages
  if (
    $('.show-content').length > 0 &&
    $('.show-content').children().length > 0
  ) {
    contentLoaded = true;
    // Discussions
  } else if (
    $('#discussion_topic').length > 0 &&
    $('.user_content').text().length > 0
  ) {
    contentLoaded = true;
    // Assignment (Teacher View)
  } else if ($('#assignment_show .teacher-version').length > 0) {
    contentLoaded = true;
  } else if ($('#assignment_show .student-version').length > 0) {
    contentLoaded = true;
  } else if ($('#course_syllabus').length > 0) {
    contentLoaded = true;
  } else if (
    $('div[data-view="users"]').length > 0 &&
    document.querySelector('tbody.collectionViewItems') !== null
  ) {
    // people page
    contentLoaded = true;
  } else if (
    $("#gradebook-grid-wrapper div[id*='assignment_'].assignment button")
      .length > 0
  ) {
    // gradebook
    contentLoaded = true;
  }

  if (contentLoaded) {
    console.log('Content has loaded');
    klAfterContentLoaded2();
  } else if (checkCount < 50) {
    const newCheckCount = checkCount + 1;
    setTimeout(() => {
      console.log(
        `Still no content, check again (${klContentWrapperElement2})`
      );
      klPageContentCheck2(klContentWrapperElement2, newCheckCount);
    }, 100);
  }
}

function klAfterContentLoaded2() {
  $(
    "a[href='https://www.asu.edu/it/acadtech/certificate/certificate.html#course=Community%20of%20Care%3A%20Coming%20to%20Campus']"
  ).attr(
    'href',
    `https://www.asu.edu/it/acadtech/certificate/certificate.html#course=Community%20of%20Care%3A%20Coming%20to%20Campus&name=${ENV.current_user.display_name}`
  );
  $(
    "a[href='https://www.asu.edu/it/acadtech/certificate/certificate.html#course=Devils%204%20Devils%3A%20Creating%20a%20Safe%20and%20Caring%20Community']"
  ).attr(
    'href',
    `https://www.asu.edu/it/acadtech/certificate/certificate.html#course=Devils%204%20Devils%3A%20Creating%20a%20Safe%20and%20Caring%20Community&name=${ENV.current_user.display_name}`
  );
  $(
    "a[href='https://www.asu.edu/it/acadtech/certificate/certificate.html']"
  ).attr(
    'href',
    `https://www.asu.edu/it/acadtech/certificate/certificate.html#name=${ENV.current_user.display_name}`
  );
  $(
    "a[href='https://www.asu.edu/it/acadtech/certificate-sustainability/certificate.html']"
  ).attr(
    'href',
    `https://www.asu.edu/it/acadtech/certificate-sustainability/certificate.html#name=${ENV.current_user.display_name}`
  );
  $(
    "a[href='https://www.asu.edu/it/acadtech/certificate/certificate.html#course=Free%20Speech%20at%20ASU']"
  ).attr(
    'href',
    `https://www.asu.edu/it/acadtech/certificate/certificate.html#course=Free%20Speech%20at%20ASU&name=${ENV.current_user.display_name}`
  );

  if ($('p#asuAdrianTermPage').length === 1) {
    asuTermUtility();
  }

  // Check if we're on the People page
  if (
    document.querySelector('tbody.collectionViewItems') !== null &&
    window.location.toString().indexOf('users') > 0
  ) {
    asuInactivePeoplePage();
    asuAddAlertForManualAdds();
  }
}

function asuTermUtility() {
  $('#asuAdrianTermPage').html(
    'Move courses that are in the default term <input type="button" id="asuMigrateTerms" value="Migrate Courses" /><br><br>Rows returned: <span id="numResults"></span><br>Courses moved: <span id="numMovedCourses"></span><br>Number of errors: <span id="numErrors"></span><table id="tableResults"></table>'
  );
  $('#asuMigrateTerms').click(() => {
    const termUrl = '/api/v1/accounts/1/terms?per_page=100';
    const termArray = [];
    // var rawData = [];
    const resultsArray = [];
    let coursesMoved = 0;
    let courseErrors = 0;
    let coursesUrl;
    let courseInfo;
    let tempTerm;
    let tempUrl;
    let tempData;
    let tblResultsTR;
    let i;
    let resultsLength;
    const processStartTime = new Date();
    const currentYear = processStartTime.getFullYear();
    // Reset display
    $('#tableResults').html(
      '<tr><th>Course Code</th><th>New Term</th><th>Status</th></tr>'
    );
    $('#numResults').html('0');
    $('#numErrors').html('0');
    $('#numMovedCourses').html('0');
    $('#asuResultsComplete').remove();

    const asuBuildTermList = (data) => {
      // Parse data to store relevant term details in an array
      data.enrollment_terms.forEach((term) => {
        termArray[term.id] = term.sis_term_id;
      });
    };

    const asuFetchProcessCourses = () => {
      // List 100 courses from the Default Term
      coursesUrl =
        '/api/v1/accounts/1/courses?per_page=100&enrollment_term_id=1';

      // Build out resultsArray
      const asuBuildCourseTermList = (data, count) => {
        // rawData = rawData.concat( data );
        console.log('Data received, loop through the courses and map them');
        $('#numResults').html(count);

        for (i = 0, resultsLength = data.length; i < resultsLength; i++) {
          // Match to term based on course Id if possible
          courseInfo = data[i].sis_course_id.slice(
            0,
            data[i].sis_course_id.indexOf('-')
          );
          console.log(`courseInfo for [${i}] = ${courseInfo}`);

          if (courseInfo.indexOf('DUPL') === 0) {
            // snip "DUPL" to find the correct term
            courseInfo = courseInfo.substr(4);
          }

          switch (courseInfo) {
            case 'DEV':
              tempTerm = termArray.indexOf(`${currentYear}DEV`);
              break;
            case 'ORG':
              tempTerm = termArray.indexOf(`${currentYear}ORG`);
              break;
            case 'TRN':
              tempTerm = termArray.indexOf(`${currentYear}TRN`);
              break;
            default:
              if (termArray.indexOf(courseInfo) > 0) {
                tempTerm = termArray.indexOf(courseInfo);
              } else if (termArray.indexOf(`${courseInfo}C`) > 0) {
                tempTerm = termArray.indexOf(`${courseInfo}C`);
              } else {
                tempTerm = -1;
                console.log('Term not found?');
              }
          }
          console.log(
            `Course [${data[i].sis_course_id}] should be in term [${termArray[tempTerm]}]`
          );

          if (tempTerm === -1) {
            // This course failed for some reason, note it on the page
            tblResultsTR = `<tr style='color: red;'><td><a href="/courses/${data[i].id}/settings">${data[i].sis_course_id}</a></td><td>Term not found</td><td>Failed</td></tr>`;
            // Output results onto page
            $('#tableResults').append(tblResultsTR);
            // Add to the error count
            courseErrors += 1;
          } else {
            // Store course details in preparation for moving it
            resultsArray.push([
              data[i].id,
              data[i].sis_course_id,
              termArray[tempTerm],
            ]);

            // Temp preview of output, comment/remove for actual processing
            // tblResultsTR = "<tr><td>" + rawData[i].sis_course_id + "</td><td>" + termArray[ tempTerm ] + "</td><td>Processing</td></tr>";
            // $("#tableResults").append( tblResultsTR );
          }
        }
        // Fill in moved and error counts
        $('#numErrors').html(courseErrors);
      };

      const asuCheckResults = () => {
        console.log(
          'Data collection complete, confirm data exists and move courses'
        );

        // Make sure we actually got results
        if (resultsArray.length === 0) {
          const processEndTime = new Date();
          const processTotalTime =
            (processEndTime.getTime() - processStartTime.getTime()) / 1000;
          $('#numResults').after(
            `<span id='asuResultsComplete' style='color: red'> - done - Complete in ${processTotalTime} seconds</span>`
          );
        } else {
          asuMoveCoursesToTerms();
        }
      };

      const asuMoveCoursesToTerms = () => {
        // Actually move the courses
        // Serialize put requests to avoid throttling
        tempUrl = `/api/v1/courses/${resultsArray[0][0]}`;
        tempData = `course[term_id]=${termArray.indexOf(resultsArray[0][2])}`;
        $.ajax({
          url: tempUrl,
          type: 'PUT',
          data: tempData,
        }).done((data, status) => {
          tblResultsTR = `<tr><td><a href="/courses/${resultsArray[0][0]}/settings">${resultsArray[0][1]}</a></td><td>${resultsArray[0][2]}</td><td>${status}</td></tr>`;
          // Output results onto page
          $('#tableResults').append(tblResultsTR);
          // Add to count of moved courses
          coursesMoved += 1;
          // Update moved course count on page
          $('#numMovedCourses').html(coursesMoved);
          resultsArray.shift();
          if (resultsArray.length > 0) {
            asuMoveCoursesToTerms();
          } else {
            const processEndTime = new Date();
            const processTotalTime =
              (processEndTime.getTime() - processStartTime.getTime()) / 1000;
            $('#numResults').after(
              `<span id='asuResultsComplete' style='color: red'> - done - Complete in ${processTotalTime} seconds</span>`
            );
          }
        });
      };

      // Usage: first time paginateAPI( url, processCallback, endingCallback )
      paginateAPI(coursesUrl, asuBuildCourseTermList, asuCheckResults);
    };

    paginateAPI(termUrl, asuBuildTermList, asuFetchProcessCourses);
  });
}

function asuInactivePeoplePage() {
  // Check if an "asuInactiveHidden" cookie exists, if not set it to false (visible)
  asuCheckInactiveCookie();

  // Create a mutationObserver that will hide inactive users when the roster list changes (if that is the current user's preference)
  const mutationObserver = new MutationObserver((mutations) => {
    mutations.forEach(() => {
      // console.log(mutation);
      // If inactive users should be hidden, hide them
      if (asuInactiveHidden) {
        asuToggleInactiveUsers();
      }
    });

    // Add click event to deactivateUser to catch new rows added to the table
    let i;
    for (
      i = 0;
      i <
      $("td.right div.admin-links ul li a[data-event='deactivateUser']").length;
      i++
    ) {
      // Check if we've set a custom attribute on the link to store its state
      if (
        !$("td.right div.admin-links ul li a[data-event='deactivateUser']")[
          i
        ].getAttribute('hasASUClickEvent')
      ) {
        // If not, then add the attribute and the event listener
        $("td.right div.admin-links ul li a[data-event='deactivateUser']")[
          i
        ].setAttribute('hasASUClickEvent', true);
        $("td.right div.admin-links ul li a[data-event='deactivateUser']")[
          i
        ].addEventListener('click', () => {
          asuCheckForNewlyDeactivatedUsers(0);
        });
        console.log(
          `adding event to ${
            $("td.right div.admin-links ul li a[data-event='deactivateUser']")[
              i
            ].parentElement.parentElement.parentElement.parentElement
              .parentElement.id
          }`
        );
      }
    }
  });

  const tableBody = document.querySelector('tbody.collectionViewItems');

  const config = { attributes: true, childList: true, characterData: true };

  mutationObserver.observe(tableBody, config);

  asuInjectHideShowButtonSelectorPosition(
    "a[aria-label='Add People']",
    'before'
  );
  asuToggleInactiveUsers();
  asuFixAlternatingRowStyling();
  asuAttachInactiveClickHandler();

  $("td.right div.admin-links ul li a[data-event='deactivateUser']").click(
    () => {
      asuCheckForNewlyDeactivatedUsers(0);
    }
  );
}

function asuCheckInactiveCookie() {
  asuInactiveHidden = getCookie('asuInactiveHidden');
  if (asuInactiveHidden === '') {
    // Default to false
    asuInactiveHidden = false;
    setCookie('asuInactiveHidden', asuInactiveHidden, 365);
  } else {
    // Convert from string to boolean
    asuInactiveHidden = asuInactiveHidden === 'true';
  }
}

let acceptButtonHitCount = 0;

async function asuAddAlertForManualAdds() {
  const currentCourseId = asuParseUrlForIdUrlSearchTerm(
    window.location.href,
    'courses'
  );

  let courseCode;

  await $.get(`/api/v1/courses/${currentCourseId}`, (data2) => {
    courseCode = data2.course_code.toUpperCase();
  });

  if (courseCode !== undefined && courseCode !== null) {
    // add student alert for manual adds only for live courses and on first click
    if (
      !courseCode.startsWith('DEV') &&
      !courseCode.startsWith('TRN') &&
      !courseCode.startsWith('ORG') &&
      !courseCode.startsWith('AU')
    ) {
      $('#addUsers').click(() => {
        if (acceptButtonHitCount < 1) {
          asuCreateAlertDiv();
        }
      });
    }
  }
}

function asuCreateAlertDiv() {
  const alertDiv = document.createElement('div');
  alertDiv.id = 'alert-content';
  alertDiv.className = 'custom-asu-alert-content';
  alertDiv.innerHTML =
    '<p style="color: whitesmoke; padding: 35px; text-align: center; font-weight: 600">The enrollment for this course is programmatically managed and any students you add manually will be removed nightly. Please reach out to the Help Center if you would like to enroll the student permanently in this course.</p>';
  const acceptButton = document.createElement('button');
  acceptButton.id = 'accept-button';
  acceptButton.innerText = 'Accept';
  acceptButton.className = 'custom-asu-btn-maroon';
  acceptButton.style.cssText = 'position: absolute; left: 41%;';
  alertDiv.appendChild(acceptButton);

  document.body.appendChild(alertDiv);
  document
    .getElementById('accept-button')
    .addEventListener('click', asuRemoveDivElement);
  const divElement = document.getElementsByClassName('addpeople__peoplesearch');
  $(divElement).before(alertDiv);
}

function asuRemoveDivElement() {
  $('#alert-content').remove();
  acceptButtonHitCount += 1;
}

function asuCheckForNewlyDeactivatedUsers(checkCount) {
  if (!asuInactiveHidden) {
    console.log('Inactive users should be visible, exiting.');
    return;
  }

  let newlyDeactivated = false;

  if (
    $("span[title='This user is currently not able to access the course']")
      .parent()
      .parent()
      .has(':visible').length > 0
  ) {
    newlyDeactivated = true;
  }

  if (newlyDeactivated) {
    asuToggleInactiveUsers();
    asuFixAlternatingRowStyling();
  } else if (checkCount < 50) {
    const newCheckCount = checkCount + 1;
    setTimeout(() => {
      asuCheckForNewlyDeactivatedUsers(newCheckCount);
    }, 100);
  }
}

function asuInjectHideShowButtonSelectorPosition(selector, position) {
  const showHtml =
    "<a href='#' class='btn btn-primary pull-right' id='asuToggleInactiveButton' role='button' title='Show Inactive' aria-label='Show Inactive' asuStatus='hidden' style='margin-left: 5px; z-index: 1;'>Show Inactive</a>";
  const hideHtml =
    "<a href='#' class='btn btn-primary pull-right' id='asuToggleInactiveButton' role='button' title='Hide Inactive' aria-label='Hide Inactive' asuStatus='visible' style='margin-left: 5px; z-index: 1;'>Hide Inactive</a>";

  if (asuInactiveHidden) {
    if (position === 'before') {
      $(selector).before(showHtml);
    } else {
      $(selector).after(showHtml);
    }
  } else if (position === 'before') {
    $(selector).before(hideHtml);
  } else {
    $(selector).after(hideHtml);
  }
}

function asuToggleInactiveUsers() {
  if (asuInactiveHidden) {
    $("span[title='This user is currently not able to access the course']")
      .parent()
      .parent()
      .hide();
  } else {
    $("span[title='This user is currently not able to access the course']")
      .parent()
      .parent()
      .show();
  }
}

function asuFixAlternatingRowStyling() {
  $('.ic-Table.ic-Table--striped tbody tr').css('background', 'inherit');
  $('.ic-Table.ic-Table--striped tbody tr:visible:odd').css(
    'background',
    '#F5F5F5'
  );
  $('.ic-Table.ic-Table--striped tbody tr').hover(
    function asuTableEvenHoverHandler(e) {
      $(this).css(
        'background-color',
        e.type === 'mouseenter' ? '#E5F2F8' : 'inherit'
      );
    }
  );
  $('.ic-Table.ic-Table--striped tbody tr:visible:odd').hover(
    function asuTableOddHoverHandler(e) {
      $(this).css(
        'background-color',
        e.type === 'mouseenter' ? '#E5F2F8' : '#F5F5F5'
      );
    }
  );
}

function asuAttachInactiveClickHandler() {
  $('#asuToggleInactiveButton').click(function asuToggleInactiveHandler() {
    if ($(this).attr('asuStatus') === 'visible') {
      $(this)
        .attr('asuStatus', 'hidden')
        .html('Show Inactive')
        .attr('aria-label', 'Show Inactive')
        .attr('title', 'Show Inactive');
      asuInactiveHidden = true;
    } else {
      $(this)
        .attr('asuStatus', 'visible')
        .html('Hide Inactive')
        .attr('aria-label', 'Hide Inactive')
        .attr('title', 'Hide Inactive');
      asuInactiveHidden = false;
    }
    asuToggleInactiveUsers();
    asuFixAlternatingRowStyling();
    // Update the cookie to their current preference
    setCookie('asuInactiveHidden', asuInactiveHidden, 365);
  });
}

function asuFilterTermsBasedOnLocation() {
  let asuCurrentAccountId;
  let asuSubAccount = 'ASU'; // default to ASU because that is most likely
  const auSubAccounts = auSubAccountIds;

  if (/accounts\/\d+($|\/$|\/?\?)/.test(window.location.href)) {
    asuDisableTermFilter();
  }

  // Decide whether we want ASU or AU terms
  const asuWhatAccountAreWeIn = new Promise((resolve) => {
    if (/courses\/\d+\/settings/.test(window.location.href)) {
      // Make API call for course and pull account id
      const currentCourseId = asuParseUrlForIdUrlSearchTerm(
        window.location.href,
        'courses'
      );
      $.get(`/api/v1/courses/${currentCourseId}`, (data) => {
        console.log(`Retrieved account id: ${data.account_id}`);
        resolve(data.account_id);
      });
    } else if (/accounts\/\d+/.test(window.location.href)) {
      // just pull account ID # from URL
      resolve(asuParseUrlForIdUrlSearchTerm(window.location.href, 'accounts'));
    }
  });

  asuWhatAccountAreWeIn.then(
    (result) => {
      asuCurrentAccountId = result;
      console.log(`We're in account: ${asuCurrentAccountId}`);
      if (auSubAccounts.indexOf(parseInt(asuCurrentAccountId, 10)) > -1) {
        console.log('Changing asuSubAccount to AU');
        asuSubAccount = 'AU';
      }
      const termUrl = '/api/v1/accounts/1/terms?per_page=100';
      const termArray = [];

      const asuBuildTermFilteringList = (data) => {
        // Parse data to store relevant term details in an array
        data.enrollment_terms.forEach((term) => {
          if (term.name.indexOf('AU') === -1) {
            termArray[term.id] = 'ASU';
          } else {
            termArray[term.id] = 'AU';
          }
        });
      };

      const asuCleanTermsOnPage = () => {
        if (/accounts\/\d+($|\/$|\/?\?)/.test(window.location.href)) {
          // For accounts > Courses, catch with mutation observer and destroy/hide unwanted spans when they're created
          // -----------------Accounts > Courses-----------------//
          const mutationObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
              let currentSpanVal;
              if (
                mutation.target.dir === 'ltr' ||
                mutation.target.localName === 'ul'
              ) {
                if (mutation.addedNodes.length !== 0) {
                  $(
                    "span[dir='ltr'] > span > span > span > div > ul > li > span > div > ul > li > span"
                  ).each(function asuShowHideTermAccountHandler() {
                    const spanItem = $(this);
                    const termHeading =
                      spanItem[0].parentNode.parentNode.parentNode.firstChild
                        .innerText;

                    // lets make sure we are only modifing the correct term list (added since we can no longer rely on list selection path above)
                    if (
                      termHeading === 'Show courses from' ||
                      termHeading === 'Active Terms' ||
                      termHeading === 'Future Terms' ||
                      termHeading === 'Past Terms'
                    ) {
                      currentSpanVal = $(this).attr('value');
                      console.log(
                        `value = ${currentSpanVal}; - asuSubAccount: [${asuSubAccount}] and termArray[this.value]: ${termArray[currentSpanVal]}`
                      );
                      if (
                        asuSubAccount === termArray[currentSpanVal] ||
                        currentSpanVal === '1'
                      ) {
                        $(this).show();
                      } else {
                        $(this).hide();
                      }

                      if ($(this).parent().id === 'asuLoading') {
                        $(this).parent().remove();
                      }
                    }
                  });
                }
              }
            });
          });

          mutationObserver.observe(document.body, {
            attributes: false,
            characterData: false,
            childList: true,
            subtree: true,
            attributeOldValue: false,
            characterDataOldValue: false,
          });

          asuEnableTermFilter();
          // -------------end Accounts > Courses----------------- //
        } else if (/courses\/\d+\/settings/.test(window.location.href)) {
          // -------------Course > Settings----------------- //
          console.log(
            `There are ${
              $('select#course_enrollment_term_id option').length
            } term options on page load`
          );
          let currentOptVal;
          $('select#course_enrollment_term_id option').each(
            function asuShowHideTermCourseHandler() {
              currentOptVal = $(this).attr('value');
              console.log(
                `value = ${currentOptVal}; - asuSubAccount: [${asuSubAccount}] and termArray[this.value]: ${termArray[currentOptVal]}`
              );
              if (
                asuSubAccount === termArray[currentOptVal] ||
                currentOptVal === '1'
              ) {
                $(this).show();
              } else {
                $(this).hide();
              }
            }
          );
          // ---------end Course > Settings----------------- //
        } else {
          // -------------Accounts > Analytics----------------- //
          console.log(
            `There are ${
              $('select.ic-Input option').length
            } term options on page load`
          );
          let currentOptVal;
          $('select.ic-Input option').each(
            function asuShowHideTermAnalyticsHandler() {
              currentOptVal = $(this).attr('value');
              console.log(
                `value = ${currentOptVal}; - asuSubAccount: [${asuSubAccount}] and termArray[this.value]: ${termArray[currentOptVal]}`
              );
              if (
                asuSubAccount === termArray[currentOptVal] ||
                currentOptVal === '1'
              ) {
                $(this).show();
              } else {
                $(this).hide();
              }

              if ($(this).parent().id === 'asuLoading') {
                $(this).parent().remove();
              }
            }
          );
          // ---------end Accounts > Analytics----------------- //
        }
      };

      paginateAPI(termUrl, asuBuildTermFilteringList, asuCleanTermsOnPage);
    },
    (error) => {
      asuCurrentAccountId = error;
    }
  );
}

function asuDisableTermFilter() {
  const filterBox = {};
  filterBox.obj = $('#termFilter')
    .parent()
    .parent()
    .parent()
    .parent()
    .parent()
    .parent()
    .parent()
    .parent()
    .parent()
    .parent()
    .parent();
  filterBox.top = filterBox.obj.offset().top;
  filterBox.left = filterBox.obj.offset().left;
  filterBox.width = filterBox.obj.css('width');
  filterBox.height = filterBox.obj.css('height');
  filterBox.paddingLeft = filterBox.obj.css('padding-left');

  $("<div id='loadingFilterBlocker'></div>").prependTo('#wrapper');
  $('#loadingFilterBlocker')
    .css('position', 'absolute')
    .css('background', 'rgba(0, 0, 0, 0.05)')
    .css('top', filterBox.top)
    .css('left', filterBox.left)
    .css('width', filterBox.width)
    .css('height', filterBox.height)
    .css('margin-left', filterBox.paddingLeft)
    .css('border-radius', 'var(--qBMHb-borderRadius)')
    .css('z-index', 11);
}

function asuEnableTermFilter() {
  $('#loadingFilterBlocker').remove();
}

window.addEventListener('load', () => {
  // PROD ONLY - Do not copy to DEV/TEST/BETA
  // MediaPlus analytics
  const elementsWithUrl = document.querySelectorAll('[src],[href]');
  const regex = /mediaplus.*\.asu\.edu\/lti\/embedded/;

  elementsWithUrl.forEach((element) => {
    const mediaplusUrl = element.src || element.href;
    if (mediaplusUrl && mediaplusUrl.match(regex)) {
      if (element.src) {
        // eslint-disable-next-line no-param-reassign
        element.src += `&userId=${window.ENV.current_user_id}`;
      } else {
        // eslint-disable-next-line no-param-reassign
        element.href += `&userId=${window.ENV.current_user_id}`;
      }
    }
  });
  // Initialize GA
  asuGA(
    window,
    document,
    'script',
    'https://www.google-analytics.com/analytics.js',
    'asu_ga'
  );

  // Fetch Canvas userId and pass with pageiew to GA
  const USER_ID = ENV.current_user_id;
  asu_ga('create', 'UA-42798992-21', 'auto', {
    userId: USER_ID,
  });
  asu_ga('send', 'pageview');

  // Check if we are on a redirect page
  if ($('#custom_url').length > 0 && $('#custom_new_tab').length === 0) {
    // Check if the redirect link is pointing to a Canvas domain
    if (
      $('#custom_url')
        .val()
        .substring(0, $('#custom_url').val().indexOf('/', 9)) ===
        'https://asu.instructure.com' ||
      $('#custom_url')
        .val()
        .substring(0, $('#custom_url').val().indexOf('/', 9)) ===
        'https://canvas.asu.edu'
    ) {
      // Compare custom_url against current domain
      if (
        window.location
          .toString()
          .substring(0, window.location.toString().indexOf('/', 9)) !==
        $('#custom_url')
          .val()
          .substring(0, $('#custom_url').val().indexOf('/', 9))
      ) {
        // Domains do not match, update custom_url to reflect current domain and set window.location to redirect
        window.location =
          window.location
            .toString()
            .substring(0, window.location.toString().indexOf('/', 9)) +
          $('#custom_url')
            .val()
            .substring($('#custom_url').val().indexOf('/', 9));
      }
    }
  }
  // END PROD ONLY - Do not copy to DEV/TEST/BETA

  // Check if we're on a course page
  if (window.location.pathname.substring(1, 8) === 'courses') {
    // Add hidden eye icon to course navigation link
    const courseNavLinks = document.querySelectorAll('#section-tabs > li > a');
    if (courseNavLinks) {
      courseNavLinks.forEach((el) => {
        switch (el.innerText) {
          // Ally Dashboard
          case 'Ally Dashboard':
            // eslint-disable-next-line no-param-reassign
            el.title = 'Not visible to students';
            // eslint-disable-next-line no-param-reassign
            el.innerHTML = `${el.innerHTML}<i class="nav-icon icon-off" aria-hidden="true" role="presentation"></i>`;
            break;

          // Rubrics
          case 'Rubrics':
            if (el.childElementCount === 0) {
              // eslint-disable-next-line no-param-reassign
              el.title = 'Not visible to students';
              // eslint-disable-next-line no-param-reassign
              el.innerHTML = `${el.innerHTML}<i class="nav-icon icon-off" aria-hidden="true" role="presentation"></i>`;
            }
            break;

          // Item Banks
          case 'Item Banks':
            if (el.childElementCount === 0) {
              // eslint-disable-next-line no-param-reassign
              el.title = 'Not visible to students';
              // eslint-disable-next-line no-param-reassign
              el.innerHTML = `${el.innerHTML}<i class="nav-icon icon-off" aria-hidden="true" role="presentation"></i>`;
            }
            break;

          default:
            break;
        }
      });
    }
  }

  // Check if we're on the course settings page
  if (window.location.pathname.endsWith('settings')) {
    // remove delete icon for CES managed sections from section tab
    const courseSections = document.getElementsByClassName('users_count');

    if (courseSections && courseSections.length > 0) {
      for (let i = 0; i < courseSections.length; i++) {
        const sectionElement = courseSections[i];

        if (sectionElement.innerText.includes('_section_')) {
          const { nextElementSibling } = sectionElement;

          if (nextElementSibling && nextElementSibling.children) {
            const nextElementSiblingChildren = nextElementSibling.children;

            if (nextElementSiblingChildren.length === 2) {
              nextElementSiblingChildren[1].remove();
            } else if (nextElementSiblingChildren.length === 1) {
              nextElementSiblingChildren[0].remove();
            }
          }
        }
      }
    }
  }

  // Check if we're on a page with term selection
  if (
    /accounts\/\d+($|\/$|\/?\?)/.test(window.location.href) ||
    /courses\/\d+\/settings/.test(window.location.href) ||
    /accounts\/\d+\/analytics/.test(window.location.href)
  ) {
    asuFilterTermsBasedOnLocation();
  }

  // Add header links to every page except speed grader and students' view of their assignment submissions or quiz submissions
  if (
    window.location.href.indexOf('submissions') === -1 &&
    window.location.href.indexOf('speed_grader') === -1 &&
    $('#speedgrader_iframe').length === 0 &&
    window.location.href.indexOf('headless') === -1
  ) {
    $(
      '<div class="asuHeaderPadding"></div><div id="custom-asu-header-links"><ul id="custom-asu-header-ul" class="closed"><li><a class="Button" href="http://www.asu.edu/">ASU Home</a></li><li><a class="Button" href="https://my.asu.edu/">My ASU</a></li><li><a class="Button" href="http://www.asu.edu/colleges/">Colleges &amp; Schools</a></li><li><a class="Button" href="http://www.asu.edu/map/">Map &amp; Locations</a></li><li><a class="Button" href="http://www.asu.edu/contactasu/">Contact Us</a></li></ul></div>'
    ).prependTo('#wrapper');
    $('button.mobile-header-hamburger:first').after(
      '<div style="position: absolute; width: 100%;"><button id="mobile-custom-asu-header-links" class="Button Button--icon-action-rev Button--large  mobile-header-hamburger"><i class="icon-solid icon-hamburger"></i><span class="screenreader-only">ASU Header Links</span></button></div>'
    );
  }

  // Add event handler to open/close the header link menu on mobile/small browsers
  $('#mobile-custom-asu-header-links').click(() => {
    if ($('#mobile-custom-asu-header-links > i').hasClass('icon-hamburger')) {
      // Currently closed, open the menu, #custom-asu-header-ul
      $('#mobile-custom-asu-header-links > i')
        .removeClass('icon-hamburger')
        .addClass('icon-x');
      $('#custom-asu-header-ul').removeClass('closed').addClass('opened');
    } else {
      // Currently open, close the menu, #custom-asu-header-ul
      $('#mobile-custom-asu-header-links > i')
        .removeClass('icon-x')
        .addClass('icon-hamburger');
      $('#custom-asu-header-ul').removeClass('opened').addClass('closed');
    }
  });

  // Remove harmful things
  $(
    'div.public_options > input#course_indexed, div.public_options > label[for="course_indexed"]'
  ).remove();
  $('div.public_options > input[name="course[indexed]"]').val('0');

  // Update 404 pages to refer students to the Help Center
  $('a.submit_error_link').before(
    `If you reached this page through a link in your course, please reach out to your instructor and include this URL ( ${window.location} ), as well as what you were attempting to do when you encountered the error.<br><br>If this link was not in a course, or you need assistance with other issues, please reach out to the ASU Help Center at 1-855-278-5080.`
  );
  $('a.submit_error_link, #submit_error_form').remove();

  // Identify which page we are on and when the content has loaded
  for (let i = 0; i <= klContentWrappersArray2.length; i++) {
    if ($(klContentWrappersArray2[i]).length > 0) {
      klPageContentCheck2(klContentWrappersArray2[i], 0);
      break;
    }
  }

  // ASU CUSTOM UNITY STYLES

  /* For Custom Accordion and Custom Tabbed Panes */
  // allow only one accordion to render
  const acc = document.getElementsByClassName('custom-asu-card-header');
  const panel = document.getElementsByClassName('custom-asu-card-body');

  for (let i = 0; i < acc.length; i++) {
    // eslint-disable-next-line func-names
    acc[i].onclick = function (event) {
      event.preventDefault();
      const setClasses = !this.classList.contains('active');
      const iTag = this.parentNode.parentNode.getElementsByTagName('i');
      asuSetClass(acc, 'active', 'remove');
      asuSetClass(panel, 'show', 'remove');
      asuSetClass(iTag, 'icon-arrow-open-up', 'remove');
      asuSetClass(iTag, 'icon-arrow-open-down', 'add');

      if (setClasses) {
        this.classList.toggle('active');
        this.nextElementSibling.classList.toggle('show');
        $(this)
          .find('i')
          .removeClass('icon-arrow-open-down')
          .addClass('icon-arrow-open-up');
      }
    };
  }

  function asuSetClass(els, className, fnName) {
    for (let i = 0; i < els.length; i++) {
      els[i].classList[fnName](className);
    }
  }

  // tabbed panes remove active class on item change
  $('.custom-asu-nav-item').click((e) => {
    e.preventDefault();
    $('.active').removeClass('active');
    $(e.currentTarget).addClass('active');
    const tabContentId = e.currentTarget.hash;
    $(tabContentId).addClass('show active');
  });

  /* End Custom Accordion and Tabbed Panes */

  function asuCreateCopyButton(highlightDiv) {
    const button = document.createElement('button');
    button.className = 'copy-code-button';
    button.type = 'button';
    button.innerText = 'Copy';
    button.style =
      'float: right; height: 35px; border-radius: 5px; color: #525252; border: solid 1px #c7cdd1;';
    button.addEventListener('click', () =>
      asuCopyCodeToClipboard(button, highlightDiv)
    );
    asuAddCopyButtonToDom(button, highlightDiv);
  }

  async function asuCopyCodeToClipboard(button, highlightDiv) {
    const codeToCopy = highlightDiv.querySelector(':last-child').innerText;
    let result;
    try {
      result = await navigator.permissions.query({ name: 'clipboard-write' });
      if (result.state === 'granted' || result.state === 'prompt') {
        await navigator.clipboard.writeText(codeToCopy);
      } else {
        asuCopyCodeBlockExecCommand(codeToCopy, highlightDiv);
      }
    } catch (_) {
      asuCopyCodeBlockExecCommand(codeToCopy, highlightDiv);
    } finally {
      asuCodeWasCopied(button);
    }
  }

  function asuCopyCodeBlockExecCommand(codeToCopy, highlightDiv) {
    const textArea = document.createElement('textArea');
    textArea.contentEditable = 'true';
    textArea.readOnly = 'false';
    textArea.className = 'copyable-text-area';
    textArea.value = codeToCopy;
    highlightDiv.insertBefore(textArea, highlightDiv.firstChild);
    const range = document.createRange();
    range.selectNodeContents(textArea);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    textArea.setSelectionRange(0, 999999);
    document.execCommand('copy');
    highlightDiv.removeChild(textArea);
  }

  // change copy text to copied when button is copied
  function asuCodeWasCopied(button) {
    button.blur();
    // eslint-disable-next-line no-param-reassign
    button.innerText = 'Copied!';
    // eslint-disable-next-line func-names
    setTimeout(function () {
      // eslint-disable-next-line no-param-reassign
      button.innerText = 'Copy';
    }, 2000);
  }

  // add copy button to the dom
  function asuAddCopyButtonToDom(button, highlightDiv) {
    highlightDiv.insertBefore(button, highlightDiv.firstChild);
    const wrapper = document.createElement('div');
    wrapper.className = 'highlight-wrapper';
    highlightDiv.parentNode.insertBefore(wrapper, highlightDiv);
    wrapper.appendChild(highlightDiv);
  }

  document
    .querySelectorAll('.custom-asu-code-highlight')
    .forEach((highlightDiv) => asuCreateCopyButton(highlightDiv));
  // END ASU CUSTOM UNITY STYLES
}); // onload end

// //////////////////////////////////////////////////////////////////////////// //
// Custom Global Nav Tray                                                       //
// //////////////////////////////////////////////////////////////////////////// //
// https://community.canvaslms.com/thread/23242-global-nav-custom-tray

(() => {
  $(document).ready(() => {
    // Set tray title here  //
    const title = 'accessibility';

    // Options are above for convenience, continue if you like //
    const tidle = title.replace(/\s/g, '_').toLowerCase();

    const menu = $('#menu');
    const icon = $('<li>', {
      id: `global_nav_${tidle}_menu`,
      class: 'ic-app-header__menu-list-item',
      html:
        `<a id="global_nav_${tidle}_link" href="https://accessibility.asu.edu/canvas-student-accessibility" class="ic-app-header__menu-list-link" target="_blank">` +
        `<div class="menu-item-icon-container" role="presentation"><span class="svg-${tidle}-holder">` +
        '<svg version="1.1" class="ic-icon-svg" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 26 26" style="enable-background:new 0 0 26 26;" xml:space="preserve"><g><path class="st0" d="M20.5,8.5c-4.5,1.7-9.8,1.7-15,0L4.6,8.3v3.2L5,11.7l0.1,0.1c1.7,0.5,3.2,0.9,4.6,1.1v9.7h3.4v-5h0.5v5h3.3 v-9.8c1.3-0.2,2.6-0.5,4.1-1.1l0.4-0.2V8.3L20.5,8.5z M15.5,11.6v9.7h-0.7v-5h-3.1v5H11v-9.7l-0.6,0c-1.3-0.2-2.7-0.5-4.4-1V10 c2.5,0.7,4.9,1.1,7.2,1.1c2.3,0,4.6-0.4,6.9-1.1v0.8c-1.2,0.4-2.5,0.7-4,0.9H15.5z"/><path class="st0" d="M13.2,9.1c1.6,0,2.8-1.3,2.8-2.9s-1.3-2.9-2.8-2.9c-1.6,0-2.9,1.3-2.9,2.9S11.6,9.1,13.2,9.1z M13.2,7.9 c-0.9,0-1.6-0.6-1.6-1.6c0-0.9,0.7-1.5,1.6-1.5c0.8,0,1.5,0.6,1.5,1.5C14.7,7.2,14.1,7.9,13.2,7.9z"/><path class="st0" d="M13,0.6C6.2,0.6,0.6,6.2,0.6,13S6.2,25.3,13,25.3S25.3,19.8,25.3,13S19.8,0.6,13,0.6z M13,24.1 c-6.1,0-11-5-11-11.1s5-11,11-11s11.1,5,11.1,11S19.1,24.1,13,24.1z"/></g></svg>' +
        `</span></div>` +
        `<div class="menu-item__text">Accessibility</div></a>`,
    });

    icon.find(`.svg-${tidle}-holder`).load(() => {
      const svg = $(this).find('svg')[0];
      const svgId = `global_nav_${tidle}_svg`;
      svg.setAttribute('id', svgId);
      svg.setAttribute(
        'class',
        'ic-icon-svg menu-item__icon ic-icon-svg--apps svg-icon-help ic-icon-svg-custom-tray'
      );
      $(`#${svgId}`).find('path').removeAttr('fill');
    });

    menu.append(icon);
  });
})();
// //////////////////////////////////////////////////////////////////////////// //
