document.querySelectorAll('.galeria-card input[type="file"]').forEach((campo) => {
    campo.addEventListener('change', () => {
        campo.setCustomValidity('');
        const arquivo = campo.files[0];
        if (!arquivo) return;
        if (!/\.(jpe?g|png|webp)$/i.test(arquivo.name)) {
            campo.setCustomValidity('Selecione uma imagem JPG, PNG ou WebP.');
        } else if (arquivo.size > 5 * 1024 * 1024) {
            campo.setCustomValidity('A imagem deve ter no máximo 5 MB.');
        }
        campo.reportValidity();
    });
});
