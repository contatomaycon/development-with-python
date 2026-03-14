document.addEventListener("DOMContentLoaded", () => {
    const productForm = document.querySelector(".validate-product");
    if (!productForm) {
        return;
    }

    productForm.addEventListener("submit", (event) => {
        const precoInput = document.getElementById("preco");
        const quantidadeInput = document.getElementById("quantidade");
        const quantidadeMinimaInput = document.getElementById("quantidade_minima");

        const preco = Number(precoInput.value);
        const quantidade = Number(quantidadeInput.value);
        const quantidadeMinima = Number(quantidadeMinimaInput.value);

        if (!Number.isFinite(preco) || preco <= 0) {
            event.preventDefault();
            alert("Preco invalido. Informe um numero maior que zero.");
            return;
        }

        if (!Number.isInteger(quantidade) || quantidade < 0) {
            event.preventDefault();
            alert("Quantidade invalida. Informe um numero inteiro maior ou igual a zero.");
            return;
        }

        if (!Number.isInteger(quantidadeMinima) || quantidadeMinima < 0) {
            event.preventDefault();
            alert("Quantidade minima invalida. Informe um numero inteiro maior ou igual a zero.");
        }
    });
});
