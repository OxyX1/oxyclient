const input = document.getElementById("url");
const placeholders = [
  "example: https://example.com",
  "example: https://crazygames.com",
  "example: https://discord.com",
  "example: https://snapchat.com",
  "example: https://chatgpt.com"
];

let index = 0;
setInterval(() => {
  input.placeholder = placeholders[index];
  index = (index + 1) % placeholders.length;
}, 2000);