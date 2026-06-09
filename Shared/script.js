// ============================================
// PLATEFORME ÉDUCATIVE - JAVASCRIPT
// Script simple pour les interactions
// ============================================

// Animation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Plateforme Éducative chargée');

    // Ajouter classe loaded aux cartes pour animation
    const cards = document.querySelectorAll('.subject-card, .lesson-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});

// Fonction pour les lecteurs audio
function initAudioPlayers() {
    const audios = document.querySelectorAll('audio');
    audios.forEach(audio => {
        audio.addEventListener('play', function() {
            console.log('Lecture audio démarrée');
        });
        audio.addEventListener('pause', function() {
            console.log('Lecture audio en pause');
        });
    });
}

// Initialiser les lecteurs
initAudioPlayers();

// Fonction pour les lecteurs vidéo
function initVideoPlayers() {
    const videos = document.querySelectorAll('video');
    videos.forEach(video => {
        video.addEventListener('play', function() {
            console.log('Lecture vidéo démarrée');
        });
        video.addEventListener('pause', function() {
            console.log('Lecture vidéo en pause');
        });
    });
}

// Initialiser les joueurs vidéo
initVideoPlayers();

// Animation au scroll
window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    if (window.scrollY > 50) {
        header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.15)';
    } else {
        header.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
    }
});