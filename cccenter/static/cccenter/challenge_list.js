/*challenge_list.js
 *
 *Page is linked to the challenge_list.html
 */

function getChallengeName(){
	$.ajax({
		url: "cccenter/getChallengeName/",
		type: "GET",
		data: {},
		dataType: 'json',
		async: true,
		success:function(data){
			$('#challengeName').text(data);
		},
		error:function(){alert('fail');}
	})
}
