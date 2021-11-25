const default_bingo_discounts = {
    active_half: 'top',
    budget: '',
    lucky_participants: '',
    usage_probability: 1,
    prices: [''],
    discounts: ['', ''],
    amounts: [],
    participants_per_lot: [],
    budget_distribution: [],
    expected_budget: '',
    total_participants: '',
    unlucky_participants: '',
}

export default {
    state: {
        bingo_discounts: default_bingo_discounts,
    },
    mutations: {
        resetBingoDiscounts(state) {
            state.bingo_discounts = default_bingo_discounts;
        },
        updateBingoDiscountsInput(state, form_input_data) {
            state.bingo_discounts = {...state.bingo_discounts, ...form_input_data}
        },
        updateBingoDiscountsOutput(state, output_json) {
            state.bingo_discounts = {...state.bingo_discounts, ...output_json}
        },
        updateBingoDiscountsRecalc(state, form_recalc_data) {
            state.bingo_discounts = {...state.bingo_discounts, ...form_recalc_data}
        },
        updateBingoDiscountsActiveHalf(state, value) {
            state.bingo_discounts.active_half = value;
        },
    },
    getters: {
        bingo_discounts_active_half(state) {
            return state.bingo_discounts.active_half;
        },
        bingo_discounts_load_data(state) {
            return {
                budget: state.bingo_discounts.budget,
                lucky_participants: state.bingo_discounts.lucky_participants,
                usage_probability: state.bingo_discounts.usage_probability,
                prices: state.bingo_discounts.prices,
                discounts: state.bingo_discounts.discounts,
            }
        },
        bingo_discounts_input_data(state) {
            return {
                budget: state.bingo_discounts.budget,
                lucky_participants: state.bingo_discounts.lucky_participants,
                usage_probability: state.bingo_discounts.usage_probability,
                prices: state.bingo_discounts.prices,
                discounts: state.bingo_discounts.discounts,
                budget_distribution: state.bingo_discounts.budget_distribution.length !== 0 ? state.bingo_discounts.budget_distribution : null,
                unlucky_participants: state.bingo_discounts.unlucky_participants !== '' ? state.bingo_discounts.unlucky_participants : null,
            }
        },
        bingo_discounts_output_data(state) {
            return {
                prices: state.bingo_discounts.prices,
                discounts: state.bingo_discounts.discounts,
                amounts: state.bingo_discounts.amounts,
                participants_per_lot: state.bingo_discounts.participants_per_lot,
            }
        },
        bingo_discounts_recalculate_data(state) {
            return {
                prices: state.bingo_discounts.prices,
                budget_distribution: state.bingo_discounts.budget_distribution,
                expected_budget: state.bingo_discounts.expected_budget,
                total_participants: state.bingo_discounts.total_participants,
                unlucky_participants: state.bingo_discounts.unlucky_participants,
            }
        },
    },
    actions: {
        bingoDiscountsReset(ctx) {
            ctx.commit('resetBingoDiscounts')
        },
        async bingoDiscountsCalculateParametersClicked(ctx,  form_input_data) {
            ctx.commit('updateBingoDiscountsInput', form_input_data)
            await this.dispatch('bingoDiscountsCalculateRequest', ctx)
            ctx.commit('updateBingoDiscountsActiveHalf', 'bottom')
        },
        async bingoDiscountsRecalculateParametersClicked(ctx,  form_recalc_data) {
            ctx.commit('updateBingoDiscountsRecalc', form_recalc_data)
            await this.dispatch('bingoDiscountsCalculateRequest', ctx)
        },
        async bingoDiscountsCalculateRequest(ctx) {
            ctx.commit('changeLoading', true)
            const url = `${ctx.getters.base_url}/bingo-discount/calculate/`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ctx.getters.bingo_discounts_input_data)
            });
            if (response.ok) {
                const json = await response.json();
                console.log(json)
                ctx.commit('updateBingoDiscountsOutput', json)
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
            ctx.commit('changeLoading', false)
        },
    }
}