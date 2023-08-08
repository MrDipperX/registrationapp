const input = document.getElementById('fields');
const tooltip = input.nextElementSibling;

input.addEventListener('mouseover', () => {
  tooltip.style.display = 'inline-block';
});

input.addEventListener('mouseout', () => {
  tooltip.style.display = 'none';
});
