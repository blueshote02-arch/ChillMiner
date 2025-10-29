let coins = 0;
let mining = false;

function startMining() {
  if (mining) return alert("Already mining...");
  mining = true;
  alert("Mining started!");
  let interval = setInterval(() => {
    coins++;
    document.getElementById("coins").innerText = "Coins: " + coins;
  }, 5000);
}

function claimReward(task) {
  let reward = 10;
  coins += reward;
  alert(`✅ Task completed! +${reward} coins`);
  document.getElementById("coins").innerText = "Coins: " + coins;
}
