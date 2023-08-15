const interestedIn = document.getElementById('interestedIn');
const interestedInHint = interestedIn.nextElementSibling;

interestedIn.addEventListener('mouseover', () => {
  interestedInHint.style.display = 'inline-block';
});

interestedIn.addEventListener('mouseout', () => {
  interestedInHint.style.display = 'none';
});


const workWith = document.getElementById('workWith');
const workWithHint = workWith.nextElementSibling;

workWith.addEventListener('mouseover', () => {
  workWithHint.style.display = 'inline-block';
});

workWith.addEventListener('mouseout', () => {
  workWithHint.style.display = 'none';
});