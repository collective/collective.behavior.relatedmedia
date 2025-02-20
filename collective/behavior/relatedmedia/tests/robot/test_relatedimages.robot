*** Settings ***

Resource    plone/app/robotframework/browser.robot
Resource    keywords.robot

Library    Remote    ${PLONE_URL}/RobotRemote

Test Setup    Run Keywords    Plone test setup
Test Teardown    Run keywords     Plone test teardown


*** Variables ***

${ASSET_FOLDER}    asset-folder
${TITLE}    An edited page
${PAGE_ID}    an-edited-page


*** Test cases ***

Scenario: A page is opened to edit
    Given a logged-in site administrator
      and a nested asset folder
      and an edited page
     Then I click the 'Related Media' tab
      and I can see relatedmedia fields
      and I select a related image
      and I select a related attachment


*** Keywords ***

# GIVEN

an edited page
    Create content
    ...    type=Document
    ...    title=${TITLE}
    Go to    ${PLONE_URL}/${PAGE_ID}/edit
    Get Text    //body    contains    Edit Page

a nested asset folder
    #
    # + Assets
    #  + Mixed
    #   - File1
    #   - Image1
    #   - Document1
    #   - News Item1
    #   + Files
    #    - File1
    #    - File2
    #    + Images
    #     - Image1
    #     - Image2
    #
    ${folder_assets_uid}=  Create content    type=Folder    title=Assets    id=${ASSET_FOLDER}

    ${folder_mixed_uid}=  Create content    type=Folder    title=Mixed    container=${folder_assets_uid}
    Create content    type=File    title=File1    container=${folder_mixed_uid}
    Create content    type=Image    title=Image1    container=${folder_mixed_uid}
    Create content    type=Document    title=Document1    container=${folder_mixed_uid}
    Create content    type=News Item    title=News Item1    container=${folder_mixed_uid}

    ${folder_files_uid}=  Create content    type=Folder    title=Files    container=${folder_mixed_uid}
    Create content    type=File    title=File1    container=${folder_files_uid}
    Create content    type=File    title=File2    container=${folder_files_uid}

    ${folder_images_uid}=  Create content    type=Folder    title=Images    container=${folder_files_uid}
    Create content    type=Image    id=image-1    title=Image1    container=${folder_images_uid}
    Create content    type=Image    id=image-2    title=Image2    container=${folder_images_uid}
    Create content    type=Image    id=image-3    title=My Image    container=${folder_images_uid}
    Create content    type=Image    id=image-4    title=Another Image    container=${folder_images_uid}

# WHEN

I can see relatedmedia fields
    Get Element States    //*[@id='formfield-form-widgets-IRelatedMediaBehavior-related_images']    contains    visible
    Get Element States    //*[@id='formfield-form-widgets-IRelatedMediaBehavior-related_attachments']    contains    visible

I click the ${tab} tab
    Click    //a[contains(text(),${tab})]

I select a related image
    # Click the select button
    Click    //div[@id="formfield-form-widgets-IRelatedMediaBehavior-related_images"]//a[contains(@class, "btn-primary")]
    # Click first element in first column
    Click item in contenbrowser column    1    1
    # Click first element in second column
    Click item in contenbrowser column    2    1
    # Click first element in third column
    Click item in contenbrowser column    3    1
    # Click the select Button in the Toolbar of column 4
    # This selects the "Image 1"
    Click    //div[contains(@class, "content-browser-wrapper")]//div[contains(@class, "levelColumns")]/div[4]/div[contains(@class, "levelToolbar")]//button[contains(@class, "btn-outline-primary")]

I select a related attachment
    # Click the select button
    Click    //div[@id="formfield-form-widgets-IRelatedMediaBehavior-related_attachments"]//a[contains(@class, "btn-primary")]
    # Click first element in first column
    Click item in contenbrowser column    1    1
    # Click first element in second column
    Click item in contenbrowser column    2    1
    # Click first element in third column
    Click item in contenbrowser column    3    2
    # Click first element in fourth column
    Click item in contenbrowser column    4    1
    # Click the select Button in the Toolbar of column 4
    # This selects the "File 1"
    Click    //div[contains(@class, "content-browser-wrapper")]//div[contains(@class, "levelColumns")]/div[5]/div[contains(@class, "levelToolbar")]//button[contains(@class, "btn-outline-primary")]


I select a linked item
    # Click the select button
    Click  //div[@id="formfield-form-widgets-remoteUrl"]//a[contains(@class, "btn-primary")]
    # Click first element in first column
    Click item in contenbrowser column    1    1
    # Click first element in second column
    Click item in contenbrowser column    2    1
    # Click first element in third column
    Click item in contenbrowser column    3    1
    # Click the select Button in the Toolbar of column 4
    # This selects the "Image 1"
    Click    //div[contains(@class, "content-browser-wrapper")]//div[contains(@class, "levelColumns")]/div[4]/div[contains(@class, "levelToolbar")]//button[contains(@class, "btn-outline-primary")]

I save the page
    Click    //button[@name="form.buttons.save"]

I click the calendar icon
    Click    //span[@id='edit_form_effectiveDate_0_popup']
    Get Element States    //div[@class='calendar']   contains    visible

I select a date using the widget
    Click    //div[@class='calendar']/table/thead/tr[2]/td[4]/div


# THEN

popup calendar should have the same date
    Get Text    //div[@class='calendar']//thead//td[@class='title']    should be    January, 2001

form dropdowns should not have the default values anymore
    ${yearLabel} =  Get Selected List Label  xpath=//select[@id='edit_form_effectiveDate_0_year']
    Should Not Be Equal  ${yearLabel}  --
    ${monthLabel} =  Get Selected List Label  xpath=//select[@id='edit_form_effectiveDate_0_month']
    Should Not Be Equal  ${monthLabel}  --
    ${dayLabel} =  Get Selected List Label  xpath=//select[@id='edit_form_effectiveDate_0_day']
    Should Not Be Equal  ${dayLabel}  --

the related item is shown in the page
    Get Element Count    //*[@id="section-related"]    should be    1

the linked item is shown in the page
    # check if the selected testfolder is linked
    Get Element Count    //a[@href='${PLONE_URL}/test-folder']    greater than    0


an overlay pops up
    Get Element Count    //div[contains(@class, 'overlay')]//input[@class='insertreference']    should be    1

the categorization tab is shown
    Get Element States    //fieldset[@id='fieldset-categorization']    contains    visible

no other tab is shown
    Get Element States    //fieldset[@id='fieldset-dates']    not contains    visible
    Get Element States    //fieldset[@id='fieldset-default']    not contains    visible
    Get Element States    //fieldset[@id='fieldset-settings']    not contains    visible

at least one other item
    Go to    ${PLONE_URL}/++add++Document
    Wait For Condition    Classes    //body    contains    patterns-loaded
    Type Text    //input[@id="form-widgets-IDublinCore-title"]    ${TITLE}
    Click    //button[@name="form.buttons.save"]
    Get Text    //body    contains    Item created
