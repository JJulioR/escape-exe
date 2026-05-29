const output = document.getElementById('output');
const commandInput = document.getElementById('command-input');
const timerDisplay = document.getElementById('timer');
let seconds = 0;
let timerInterval = null;
let gameStarted = false;
let playerName = "Anonymous";
let playerId = "???";

/* Affiche un message dans le terminal lettre par lettre
   text : le texte à afficher
   callback : fonction à exécuter quand l'effet est terminé (optionnel) */

function typeWriter(text, callback) {
    // Sépare le texte en lignes sur les \n
    const lines = text.split('\n');
    let lineIndex = 0; // index pour parcourir les lignes

    function typeLine() {
        if (lineIndex >= lines.length) {
            if (callback) callback(); // exécute callback si défini
            return;
        }

        const p = document.createElement('p'); // crée ligne p
        output.appendChild(p);
        const line = lines[lineIndex];
        lineIndex++;

        // Ligne vide → passe à la suivante directement
        if (line === '') {
            output.scrollTop = output.scrollHeight; // scroll automatique
            typeLine();
            return;
        }

        let i = 0; // index pour parcourir le texte
        const interval = setInterval(() => {
            p.textContent += line[i]; // ajoute lettre par lettre
            i++;
            output.scrollTop = output.scrollHeight; // scroll automatique
            if (i >= line.length) {
                clearInterval(interval); // stop l'effet quand texte complet
                typeLine(); // passe à la ligne suivante
            }
        }, 35); // vitesse en ms
    }

    typeLine();
}

 /* ligne vide spérer les commandes */
 function addEmptyLine() {
    const p = document.createElement('p');
    p.textContent = '';
    output.appendChild(p);
 }

 /* Affiche la commande tapée par le joueur dans l'output
   pour qu'il voie ce qu'il a tap */
function printCommand(cmd) {
    const p = document.createElement('p');
    p.textContent = '> ' + cmd; //affiche la commande 
    output.appendChild(p);
}

//Timer
function startTimer() {
    timerInterval = setInterval(() => {
        seconds++;
        //convertit les secondes en MM:SS format
        const minutes = Math.floor(seconds / 60)
        const secs = seconds % 60;

        //ajt un zéro devant si < 10 (ex: 09 au lieu de 9)
        const display = String(minutes).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
        timerDisplay.textContent = 'TIME: ' + display; //affiche timer
    }, 1000); //update chaque sec
}

function stopTimer() {
    clearInterval(timerInterval); //arrête timer
}

/* Envoie une commande au serveur et retourne la réponse
   cmd : la commande à envoyer
   retourne une promesse qui résout la réponse du serveur */

/* Affiche l'écran de victoire */
async function showVictoryScreen() {
    // Calcule le temps final
    const minutes = String(Math.floor(seconds / 60)).padStart(2, '0');
    const secs = String(seconds % 60).padStart(2, '0');
    const finalTime = `${minutes}:${secs}`;

    // Vide l'output et cache la saisie
    output.innerHTML = '';
    document.getElementById('input-line').style.display = 'none';

    // Fonction utilitaire pour attendre X ms
    const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    // Affiche les lignes une par une avec des pauses
    await new Promise(r => typeWriter('=======================================', r));
    await wait(300);
    await new Promise(r => typeWriter('   SYSTEM BREACH COMPLETE', r));
    await wait(300);
    await new Promise(r => typeWriter('=======================================', r));
    await wait(300);
    await new Promise(r => typeWriter(`   ESCAPE TIME : ${finalTime}`, r));
    await wait(300);
    await new Promise(r => typeWriter(`   OPERATOR    : ${playerName}`, r));
    await wait(300);
    await new Promise(r => typeWriter(`   PLAYER ID   : ${playerId}`, r));
    await wait(300);
    await new Promise(r => typeWriter('=======================================', r));
    await wait(300);

    // Ajoute le lien cliquable
    const p = document.createElement('p');
    p.innerHTML = '   <a href="https://jrinvil.com/escape_exe/leaderboard.php" target="_blank" style="color:#00ff00; text-decoration:none;">» VIEW LEADERBOARD «</a>';
    output.appendChild(p);

    await wait(500);
    await new Promise(r => typeWriter('=======================================', r));
    await wait(300);
    await new Promise(r => typeWriter('   Type "restart" to play again. If you want to reset, reload the page', r));

    // Réactive la saisie en mode restart
    document.getElementById('input-line').style.display = 'flex';
    commandInput.dataset.mode = "restart";

    
}

async function sendCommand(cmd) {
    try{
        const response = await fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: cmd, seconds: seconds }) //envoie aussi le temps écoulé pour le scoring
        });
        const data = await response.json(); //convert rep en JSOn

        if (data.message.includes("SYSTEM BREACH COMPLETE")) {
            stopTimer(); //arrête timer si le joueur a gagné
            showVictoryScreen();
        }else{
            typeWriter(data.message); //affiche message du serveur
        }
    } catch (error) {
        typeWriter('An error occurred while processing your command.'); //affiche message d'erreur
    }
}



commandInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { // si touche entrée
        const input = commandInput.value.trim(); // récupère la saisie
        if (!input) return; // ignore si champ vide

        // Mode username — enregistre le pseudo avant de jouer
        if (commandInput.dataset.mode === "username") {
            printCommand(input); // affiche le pseudo tapé
            commandInput.value = ''; // vide le champ
            addEmptyLine(); // ajoute ligne vide
            registerPlayer(input); // envoie le pseudo au serveur
            return; // stop ici, pas de commande à envoyer
        }

        // Mode normal — envoie une commande au jeu
        const cmd = input.toLowerCase(); // met en minuscule
        printCommand(cmd); // affiche la commande dans le terminal

        if (!gameStarted && cmd === "start") { // si c'est la première commande "start"
            gameStarted = true; // marque le début du jeu
            startTimer(); // démarre le timer
        }
        // Mode restart — relance le jeu
        if (commandInput.dataset.mode === "restart") {
             if (input.toLowerCase() === "restart") {
                output.innerHTML = '';
                seconds = 0;
                gameStarted = false;
                timerDisplay.textContent = 'TIME: 00:00';
                commandInput.dataset.mode = "command";
                document.getElementById('input-line').style.display = 'flex';
                sendCommand('start');
             }
             return;
        }


        sendCommand(cmd); // envoie commande au serveur
        commandInput.value = ''; // vide le champ de saisie
        addEmptyLine(); // ajoute ligne vide après chaque commande
    }
});

//msg de bienvenue
document.addEventListener('DOMContentLoaded', () => {
    typeWriter('ESCAPE.EXE - INITIALIZING...', () => {
        setTimeout(() => {
            typeWriter('IDENTIFY YOURSELF, OPERATOR.', () => {
                setTimeout(() => {

                    promptUsername();
                }, 500);
            });
        }, 500);
    });
});

// Demande le pseudo avant de start
function promptUsername() {
    typeWriter('Enter your username and press ENTER:');
    
    // Mode "username" — le prochain Enter enregistre le pseudo
    commandInput.dataset.mode = "username";
}

// Enregistre pseudo via l'API Flask
async function registerPlayer(username) {
    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username })
        });
        const data = await response.json();

        playerName = data.username; // stocke pseudo pour écran de victoire
        playerId = data.player_id; // stocke ID pour écran de victoire

        // Affiche l'ID du joueur
        typeWriter(`Welcome, ${data.username}!`, () => {
            setTimeout(() => {
                typeWriter(`Your player ID: ${data.player_id} — share it with a friend! or don't I'm not your master...`, () => {
                    setTimeout(() => {
                        typeWriter('Type "start" to begin your escape. OR type "help" for commands.'); // invite à taper start ou help
                        // Repasse en mode normal
                        commandInput.dataset.mode = "command";
                    }, 500);
                });
            }, 300);
        });

    } catch (error) {
        typeWriter('ERROR: Could not register. Type "start" to play as Anonymous.');
        commandInput.dataset.mode = "command";
    }
}