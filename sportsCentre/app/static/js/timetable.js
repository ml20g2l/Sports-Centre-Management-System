// Set background colour and text colour for all swimming pool team events cells
const swimmingPoolCell = document.querySelectorAll('.swimming-pool.team-events');
swimmingPoolCell.forEach(cell => {
  cell.style.backgroundColor = "#1E90FF";
  cell.style.color = "#fff";
});

// Set background colour and text colour for all sports hall team events cells
const sportsHallCell = document.querySelectorAll('.sports-hall.team-events');
sportsHallCell.forEach(cell => {
  cell.style.backgroundColor = "#008B8B";
  cell.style.color = "#fff";
});

// Set background colour and text colour for the pilates cell
const pilatesCell = document.querySelector('.pilates');
pilatesCell.style.backgroundColor = "#9932CC";
pilatesCell.style.color = "#fff";

// Set background colour and text colour for all sports hall aerobics team events cells
const sportshallaerobics = document.querySelectorAll('.sports-hall-aerobics.team-events');
sportshallaerobics.forEach(cell => {
  cell.style.backgroundColor = "#2F4F4F";
  cell.style.color = "#fff";
});

// Set background colour and text colour for all aerobics cells
const AerobicsCell = document.querySelectorAll('.aerobics');
AerobicsCell.forEach(cell => {
  cell.style.backgroundColor = "#8B0000";
  cell.style.color = "#fff";
});
