export default {
    state: {
        active_half: 'top',
        lot_cost: {
            cheap: '',
            middle: '',
            costly: '',
        },
        loyality: '',
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
            min: '',
            cur: '',
            max: ''
        }
    },
    mutations: {
        updateActiveHalf(state, value) {
            state.active_half = value;
        },
        updateCost(state, value) {
            state.lot_cost = value;
        },
        updateLoyality(state, value) {
            state.loyality = value;
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
    actions: {
        async calculateParametersClicked(ctx, input_data) {
            if (input_data.lot_cost.cheap === '' || input_data.lot_cost.middle === '' || input_data.lot_cost.costly === '' ) {
                return 'цены лотов не могут быть пустыми'
            }
            ctx.commit('updateCost', input_data.lot_cost)
            ctx.commit('updateLoyality', input_data.loyality)
            ctx.commit('updateRentability', input_data.rentability)
            ctx.commit('updateCostlyAmount', input_data.costly_amount)
            ctx.commit('updateActiveHalf', 'bottom')
            let response = {
                probabilities: {cheap: 0.6, middle: 0.3, costly: 0.6},
                amounts: {cheap: 600, middle: 300, costly: 600},
                black_box_cost: {min: 500, cur: 1000, max:1500}
            }
            ctx.commit('updatePercents', response.probabilities)
            ctx.commit('updateAmounts', response.amounts)
            ctx.commit('updateBlackBoxCost', response.black_box_cost)
            return ''
        }
    },
    getters: {
        active_half(state) {
            return state.active_half;
        },
        output_data(state) {
            return {
                percents: state.percents,
                amounts: state.amounts,
                black_box_cost: state.black_box_cost,
            }
        }
    }
}