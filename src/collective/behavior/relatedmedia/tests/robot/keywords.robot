*** Keywords ***

# GIVEN

a logged-in manager
    Enable autologin as
    ...    Manager

a logged-in member
    Enable autologin as
    ...    Member

a logged-in site administrator
    Enable autologin as
    ...    Site Administrator
    ...    Contributor
    ...    Reviewer


a document '${title}'
    Create content
    ...    type=Document
    ...    id=doc
    ...    title=${title}

Click item in contenbrowser column
    [arguments]  ${colnumber}    ${itemposition}
    Wait For Condition    Element States    //div[contains(@class, "content-browser-wrapper")]//div[contains(@class, "levelColumns")]/div[${colnumber}]/div[contains(@class, "levelItems")]/div[${itemposition}]    contains    visible
    Click    //div[contains(@class, "content-browser-wrapper")]//div[contains(@class, "levelColumns")]/div[${colnumber}]/div[contains(@class, "levelItems")]/div[${itemposition}]
