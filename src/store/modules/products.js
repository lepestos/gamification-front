export default {
    state: {
        products: [],
    },
    mutations: {
        updateProducts(state, value) {
            state.products = value;
        },
    },
    getters: {
        products(state) {
            return state.products;
        },
    },
    actions: {
        async loadProducts(ctx) {
            const url = `${ctx.getters.base_url}/product/`;
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            });
            if (response.ok) {
                const json = await response.json();
                console.log(json)
                ctx.commit('updateProducts', json)
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
        },
    }
}