// =============================|
// Static configuration values: |
// =============================|
var generateQuestionUrl = "http://localhost:5000/api/v1/generate_question";
var validateAnswerUrl = "http://localhost:5000/api/v1/validate_answer";
var statisticSettingsUrl = "http://localhost:5000/api/v1/get_statistic_settings"
var correctHexColor = "#D2F5C9";
var incorrectHexColor = "#FFBBB8";

// ==================|
// Global variables: |
// ==================|
var answerStreak = 0;

var questionType = null;
var division = null;
var team = null;
var player = null;
var position = null;
var chosenValue = null;

// On-load, automatically trigger a new question
// + answers to be refreshed:
$(function() {
	getCurrentStatisticSettings();
	generateQuestion();
	updateStreak(false);
});

// ===============================================|
// Set footer with details for the current season |
// frame-of-reference being used by the server:   |
// ===============================================|
function getCurrentStatisticSettings() {
	$.ajax({
		url: statisticSettingsUrl,
		type: 'GET',
		success: function(msg) {
			label = "( currently using data for: <b>" + msg.year + " " + 
				msg.season_type + " season, week " + msg.season_week + 
				"</b> ) / gridiron v" + msg.version_info;
			$("#configurationInfo").html(label);
		}
	});
}

// ============================================|
// Request a new question + answer type from a |
// random set of eligible types:               |
// ============================================|
function generateQuestion() {
	clearVariables();

	$.ajax({
		url: generateQuestionUrl,
		type: 'GET',
		success: function(msg) {
			questionType = msg.type;

			// Store additional parameter potentially needed
			// for API validation phase:
			switch(msg.type) {
				case "TEAM_CONFERENCE":
				case "TEAM_DIVISION":
					team = msg.team;
					break;
				case "PLAYER_TEAM":
					player = msg.player;
					break;
				case "PLAYER_POSITION":
					position = msg.position;
					break;
				case "DIVISION_TEAM":
					division = msg.division;
					break;
			}

			$("#question").text(msg.question);

			// Clear the previous state to set up for the new
			// batch of tentative question answers:
			$("#options").empty();

			// Iterate through given options to [re-]populate
			// possible answer values:
			for (const option of msg.options) {
				var button = $('<input class="button" type="submit" value="' + option + '" style="width:100%;" onclick="validateAnswer(this);"/>');
				$("#options").append(button);
			}
		}
	});
}

// =======================================|
// Validate an answer tapped / clicked by |
// the user:                              |
// =======================================|
function validateAnswer(button) {
	chosenValue = button.value;

	// Generate POST data based on questionType:
	data = { "type": questionType, "options": [] };

	// Gather all tentative 'answer' / button data:
	$('#options').children('input').each(function() {
		switch(questionType) {
			case "TEAM_CONFERENCE":
			case "TEAM_DIVISION":
				data['team'] = team;
				data['options'].push(this.value);
				break;
			case "PLAYER_TEAM":
				data['player'] = player;
				data['options'].push(this.value);
				break;
			case "PLAYER_POSITION":
				data['position'] = position;
				data['options'].push(this.value);
				break;
			case "DIVISION_TEAM":
				data['division'] = division;
				data['options'].push(this.value);
				break;
		}
	});

	var shouldIncrement = false;

	// Send tentative answer(s) along for validation &
	// update / disable button selections appropriately:
	$.ajax({
		url: validateAnswerUrl,
		type: 'POST',
		data: JSON.stringify(data),
		contentType: "application/json",
		success: function(msg) {
			$.each(msg.answers, function(key, value) {
				if (value) {
					if (chosenValue === key) shouldIncrement = true;
					$('input[value="' + key + '"]').css('background-color', correctHexColor).prop("disabled", true);
				} else {
					$('input[value="' + key + '"]').css('background-color', incorrectHexColor).prop("disabled", true);;
				}
			});

			// Increment or reset counter based on 
			// last-stored value:
			updateStreak(shouldIncrement);
		}
	});

	// Start timer, wait, & then automatically
	// pull new question:
	setTimeout(function() {
		generateQuestion()
	}, 3000);
}

// =======================================|
// Utility function to clear any relevant |
// question- and answer-related variables:|
// =======================================|
function clearVariables() {
	questionType = division = team = player = position = chosenValue = null;
}

// ===================================|
// Utility function to update current |
// local 'answered-correctly' streak: |
// ===================================|
function updateStreak(shouldIncrement) {
	answerStreak = shouldIncrement ? answerStreak + 1 : 0;
	$("#streak-counter").text("🔥 " + answerStreak);
}