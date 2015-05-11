/* notification.js
 *
 * This page is linked to all the pages of the website to constantly see if a user has clicked on the new notifications
 */

function notification_clicked(notification_id) {
    // Javascript code for when a notification is clicked we want to get its id and
    // set that that notification has been viewed in the model. 
    $.ajax({
        url: "/cccenter/notificationsupdate/",
        type: "GET",
        data: {'notification_id': notification_id},
    });
}
