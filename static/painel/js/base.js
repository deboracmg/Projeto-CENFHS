// Sidebar
const menuToggles = document.querySelectorAll(".menu-toggle");
const submenuLinks = document.querySelectorAll(".sidebar-menu a");

// Abre/fecha os menus ao clicar na opção principal
menuToggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
        const menuGroup = toggle.parentElement;

        document.querySelectorAll(".menu-group").forEach((group) => {
            if (group !== menuGroup) {
                group.classList.remove("active");
            }
        });

        menuGroup.classList.toggle("active");
    });
});

// Verifica qual página está selecionada
const currentPath = window.location.pathname;

submenuLinks.forEach((link) => {
    const linkPath = link.getAttribute("href");

    if (linkPath === currentPath) {
        link.classList.add("selected");

        const menuGroup = link.closest(".menu-group");

        if (menuGroup) {
            menuGroup.classList.add("active");
        }
    }
});

// Header e Menu do Usuário
const userButton = document.querySelector(".user-button");
const userMenu = document.querySelector(".user-menu");

if (userButton && userMenu) {
    userButton.addEventListener("click", (event) => {
        event.stopPropagation();
        userMenu.classList.toggle("active");
    });

    document.addEventListener("click", (event) => {
        if (!userMenu.contains(event.target)) {
            userMenu.classList.remove("active");
        }
    });
}

// Validação das regras de senha do Django no cliente
function calcularSimilaridadeSequencia(a, b) {
    if (!a || !b) return 0;
    if (a === b) return 1;

    const lenA = a.length;
    const lenB = b.length;
    const matriz = Array.from({ length: lenA + 1 }, () =>
        new Array(lenB + 1).fill(0),
    );

    for (let i = 1; i <= lenA; i++) {
        for (let j = 1; j <= lenB; j++) {
            if (a[i - 1] === b[j - 1]) {
                matriz[i][j] = matriz[i - 1][j - 1] + 1;
            } else {
                matriz[i][j] = Math.max(matriz[i - 1][j], matriz[i][j - 1]);
            }
        }
    }

    const lcs = matriz[lenA][lenB];
    return (2.0 * lcs) / (lenA + lenB);
}

function senhaSimilarDadosPessoais(senha, valoresPessoais) {
    const senhaLimpa = senha.trim().toLowerCase();
    if (!senhaLimpa) return false;

    for (const valor of valoresPessoais) {
        const texto = (valor || "").trim().toLowerCase();
        if (!texto) continue;

        const partes = texto.split(/[\s@.+_-]+/).concat([texto]);
        for (const parte of partes) {
            if (!parte || parte.length < 3) continue;
            if (calcularSimilaridadeSequencia(senhaLimpa, parte) >= 0.7) {
                return true;
            }
        }
    }

    return false;
}

// Modal Meu Perfil
const modalPerfil = document.getElementById("modalPerfil");
const formPerfil = document.getElementById("formPerfil");
const btnAbrirPerfil = document.getElementById("btnAbrirPerfil");
const btnFecharPerfil = document.getElementById("btnFecharPerfil");
const btnAlterarSenha = document.getElementById("btnAlterarSenha");
const btnSalvarPerfil = document.getElementById("btnSalvarPerfil");

if (btnAbrirPerfil && modalPerfil && formPerfil && btnSalvarPerfil) {
    const campoNome = document.getElementById("perfil_nome");
    const campoUsername = document.getElementById("perfil_username");
    const campoEmail = document.getElementById("perfil_email");
    const secaoAlterarSenha = document.getElementById("secaoAlterarSenha");
    const campoSenhaAtual = document.getElementById("senha_atual");
    const campoNovaSenha = document.getElementById("nova_senha");
    const campoConfirmarSenha = document.getElementById("confirmar_nova_senha");
    const listaRequisitos = document.getElementById("requisitosSenha");

    let dadosOriginaisPerfil = { nome: "", username: "", email: "" };
    let alterandoSenha = false;

    function definirObrigatoriedadeCamposSenha(obrigatorio) {
        campoSenhaAtual.required = obrigatorio;
        campoNovaSenha.required = obrigatorio;
        campoConfirmarSenha.required = obrigatorio;
    }

    function ocultarSecaoSenha() {
        alterandoSenha = false;
        secaoAlterarSenha.hidden = true;
        listaRequisitos.hidden = true;
        btnAlterarSenha.hidden = false;
        campoSenhaAtual.value = "";
        campoNovaSenha.value = "";
        campoConfirmarSenha.value = "";
        definirObrigatoriedadeCamposSenha(false);
    }

    function atualizarItemRequisito(chave, atendido) {
        const item = listaRequisitos?.querySelector(`[data-requisito="${chave}"]`);
        if (!item) return;

        item.classList.toggle("atendido", atendido);
        const icone = item.querySelector("i");
        if (icone) {
            icone.className = atendido
                ? "fa-solid fa-circle-check"
                : "fa-solid fa-circle-xmark";
        }
    }

    function avaliarRequisitosPerfil() {
        const nome = campoNome.value.trim();
        const username = campoUsername.value.trim();
        const email = campoEmail.value.trim();
        const novaSenha = campoNovaSenha.value;
        const confirmarSenha = campoConfirmarSenha.value;

        const dadosContaValidos = Boolean(nome && username && email);
        const alterouDadosConta =
            nome !== dadosOriginaisPerfil.nome ||
            username !== dadosOriginaisPerfil.username ||
            email !== dadosOriginaisPerfil.email;

        const reqTamanho = novaSenha.length >= 8;
        const reqNumerica = novaSenha.length > 0 && !/^\d+$/.test(novaSenha);
        const reqSimilaridade =
            novaSenha.length > 0 &&
            !senhaSimilarDadosPessoais(novaSenha, [nome, username, email]);
        const reqConfirmacao =
            novaSenha.length > 0 && novaSenha === confirmarSenha;

        atualizarItemRequisito("tamanho", reqTamanho);
        atualizarItemRequisito("numerica", reqNumerica);
        atualizarItemRequisito("similaridade", reqSimilaridade);
        atualizarItemRequisito("confirmacao", reqConfirmacao);

        const todosRequisitosSenha =
            reqTamanho &&
            reqNumerica &&
            reqSimilaridade &&
            reqConfirmacao;

        if (alterandoSenha) {
            btnSalvarPerfil.disabled = !(dadosContaValidos && todosRequisitosSenha);
        } else {
            btnSalvarPerfil.disabled = !(dadosContaValidos && alterouDadosConta);
        }
    }

    [
        campoNome,
        campoUsername,
        campoEmail,
        campoSenhaAtual,
        campoNovaSenha,
        campoConfirmarSenha,
    ].forEach((campo) => {
        campo.addEventListener("input", avaliarRequisitosPerfil);
    });

    btnAlterarSenha?.addEventListener("click", () => {
        alterandoSenha = true;
        secaoAlterarSenha.hidden = false;
        listaRequisitos.hidden = false;
        btnAlterarSenha.hidden = true;
        definirObrigatoriedadeCamposSenha(true);
        avaliarRequisitosPerfil();
        campoSenhaAtual.focus();
    });

    btnAbrirPerfil.addEventListener("click", async () => {
        userMenu.classList.remove("active");

        try {
            const response = await fetch("/dashboard/perfil/");

            if (response.redirected && response.url.includes("/entrar/")) {
                window.location.href = response.url;
                return;
            }

            if (!response.ok) {
                throw new Error("Não foi possível carregar os dados do perfil.");
            }

            const perfil = await response.json();
            formPerfil.reset();
            formPerfil.classList.remove("com-erro");
            ocultarSecaoSenha();

            campoNome.value = perfil.nome || "";
            campoUsername.value = perfil.username || "";
            campoEmail.value = perfil.email || "";
            dadosOriginaisPerfil = {
                nome: campoNome.value.trim(),
                username: campoUsername.value.trim(),
                email: campoEmail.value.trim(),
            };

            document.getElementById("subtituloPerfil").textContent =
                `Perfil de acesso: ${perfil.perfil}`;

            avaliarRequisitosPerfil();
            modalPerfil.showModal();
        } catch (erro) {
            exibirNotificacao(erro.message, "erro");
        }
    });

    btnFecharPerfil.addEventListener("click", () => modalPerfil.close());

    formPerfil.addEventListener("submit", async (event) => {
        event.preventDefault();
        const conteudoOriginalBotao = btnSalvarPerfil.innerHTML;

        try {
            formPerfil.classList.remove("com-erro");
            checarFormulario(formPerfil);

            btnSalvarPerfil.disabled = true;
            btnSalvarPerfil.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i> Salvando...';

            const dados = await salvarCadastro(
                "/dashboard/perfil/salvar/",
                new FormData(formPerfil),
            );

            if (!dados) return;

            const saudacao = document.getElementById("saudacaoUsuario");
            if (saudacao && dados.saudacao) {
                saudacao.textContent = `Olá, ${dados.saudacao}!`;
            }

            modalPerfil.close();
            exibirNotificacao(dados.mensagem, "sucesso");
        } catch (erro) {
            exibirNotificacao(erro.message, "erro");
            avaliarRequisitosPerfil();
        } finally {
            btnSalvarPerfil.innerHTML = conteudoOriginalBotao;
        }
    });
}
