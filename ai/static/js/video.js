function playVideo(container) {
    // Trouver les éléments correspondants à l'intérieur du conteneur cliqué
    const cover = container.querySelector('.video-cover');
    const playButton = container.querySelector('.play-button');
    const video = container.parentElement.querySelector('.video-player');

    // Cacher l'image de couverture et le bouton Play
    cover.style.display = 'none';
    playButton.style.display = 'none';

    // Afficher la vidéo et ajuster la taille
    video.style.height = '300px'; // Ajuste la hauteur à tes besoins
    video.style.display = 'block';
}