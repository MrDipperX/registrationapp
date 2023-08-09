// script.js
function showAdditionalFields() {
    const roleSelect = document.getElementById('role');
    const additionalFields = document.getElementById('additionalFields');
    // const additionalFieldsInvestor = document.getElementById('additionalFieldsInvestor');
    // const additionalFieldsStartup = document.getElementById('additionalFieldsStartup');
    const startupNameInput = document.getElementById('startupName');
    const startupDescriptionInput = document.getElementById('startupDescription');
    // const startupHint = document.getElementById('startuppHint')
    // const othersHint = document.getElementById('othersHint')
    //
    // const input = document.getElementById('fields');

    if (roleSelect.value === 'Startupper') {
        // additionalFieldsInvestor.style.display = 'none';
        // additionalFieldsStartup.style.display = 'block';

        // othersHint.style.display = 'none'
        // startupHint.style.display = 'inline-block'

        additionalFields.style.display = 'block';
        startupNameInput.required = true;
        startupDescriptionInput.required = true;

        //
        // input.addEventListener('mouseover', () => {
        //   startupHint.style.display = 'inline-block';
        //   othersHint.style.display = 'none';
        // });
        //
        // input.addEventListener('mouseout', () => {
        //   startupHint.style.display = 'none';
        //   othersHint.style.display = 'none';
        // });
    } else{
        // additionalFieldsInvestor.style.display = 'block';
        // additionalFieldsStartup.style.display = 'none';

        // othersHint.style.display = 'inline-block'
        // startupHint.style.display = 'none'

        additionalFields.style.display = 'none';
        startupNameInput.required = false;
        startupDescriptionInput.required = false;


        // input.addEventListener('mouseover', () => {
        //     startupHint.style.display = 'none';
        //     othersHint.style.display = 'inline-block';
        // });
        //
        // input.addEventListener('mouseout', () => {
        //     startupHint.style.display = 'none';
        //     othersHint.style.display = 'none';
        // });
    }
}


