export default {
    state: {
        active_half: 'top',
        lot_cost: {
            cheap: '',
            middle: '',
            costly: '',
        },
        loyalty: '',
        rentability: '',
        amounts: {
            cheap: '',
            middle: '',
            costly: '',
        },
        percents: {
            cheap: '',
            middle: '',
            costly: '',
        },
        black_box_cost: {
            min: 0,
            cur: 0,
            max: 0
        }
    },
    mutations: {
        updateActiveHalf(state, value) {
            state.active_half = value;
        },
        updateCost(state, value) {
            state.lot_cost = value;
        },
        updateLoyalty(state, value) {
            state.loyalty = value;
        },
        updateRentability(state, value) {
            state.rentability = value;
        },
        updateCostlyAmount(state, value) {
            state.amounts.costly = value;
        },
        updatePercents(state, value) {
           state.percents = value;
        },
        updateAmounts(state, value) {
           state.amounts = value;
        },
        updateBlackBoxCost(state, value) {
           state.black_box_cost = value;
        }
    },
    getters: {
        active_half(state) {
            return state.active_half;
        },
        input_data(state) {
            return {
                lot_cost: state.lot_cost,
                loyalty: state.loyalty,
                rentability: state.rentability,
                costly_amount: state.amounts.costly,
                black_box_cost: state.black_box_cost.cur,
            }
        },
        output_data(state) {
            return {
                percents: state.percents,
                amounts: state.amounts,
                black_box_cost: state.black_box_cost,
            }
        },
        recalculate_data(state) {
            return {
                loyalty: state.loyalty,
                rentability: state.rentability,
                black_box_cost: state.black_box_cost,
            }
        }
    },
    actions: {
        async calculateParametersClicked(ctx,  form_input_data) {
            ctx.commit('updateCost', form_input_data.lot_cost)
            ctx.commit('updateLoyalty', form_input_data.loyalty)
            ctx.commit('updateRentability', form_input_data.rentability)
            ctx.commit('updateCostlyAmount', form_input_data.costly_amount)

            console.log(ctx.getters.input_data)
            const url = "http://localhost:8000/api/v1/black-box/calculate/";
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ctx.getters.input_data)
            });
            if (response.ok) {
                const json = await response.json();
                console.log(json)
                ctx.commit('updatePercents', json.probabilities)
                ctx.commit('updateAmounts', json.amounts)
                ctx.commit('updateBlackBoxCost', json.black_box_cost)
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
            ctx.commit('updateActiveHalf', 'bottom')
        }
    }
}