// script.js
function showAdditionalFields() {
    const roleSelect = document.getElementById('role');
    const additionalFields = document.getElementById('additionalFields');
    const additionalFieldsInvestor = document.getElementById('additionalFieldsInvestor');
    const additionalFieldsStartup = document.getElementById('additionalFieldsStartup');
    const startupNameInput = document.getElementById('startupName');
    const startupDescriptionInput = document.getElementById('startupDescription');

    if (roleSelect.value === 'Startupper') {
        additionalFieldsInvestor.style.display = 'none';
        additionalFieldsStartup.style.display = 'block';
        additionalFields.style.display = 'block';
        startupNameInput.required = true;
        startupDescriptionInput.required = true;
    } else {
        additionalFieldsInvestor.style.display = 'block';
        additionalFieldsStartup.style.display = 'none';
        additionalFields.style.display = 'none';
        startupNameInput.required = false;
        startupDescriptionInput.required = false;
    }
}
