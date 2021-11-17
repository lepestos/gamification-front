const default_black_box = {
    active_half: 'top',
    lot_cost: {
        cheap: '',
        middle: '',
        costly: '',
    },
    loyalty: 0.6,
    rentability: 0.15,
    costly_amount: '',
    amounts: {
        cheap: '',
        middle: '',
        costly: '',
    },
    probabilities: {
        cheap: '',
        middle: '',
        costly: '',
    },
    black_box_cost: {
        min: '',
        cur: '',
        max: ''
    },
    message: '',
    black_box_name: '',
}

export default {
    state: {
        black_box: default_black_box,
        saved_black_boxes: []
    },
    mutations: {
        resetBlackBox(state) {
            state.black_box = default_black_box;
        },
        updateBlackBoxInput(state, form_input_data) {
            state.black_box = {...state.black_box, ...form_input_data}
        },
        updateBlackBoxOutput(state, output_json) {
            state.black_box = {...state.black_box, ...output_json}
        },
        updateBlackBoxRecalc(state, form_recalc_data) {
            state.black_box = {...state.black_box, ...form_recalc_data}
        },
        updateBlackBoxActiveHalf(state, value) {
            state.black_box.active_half = value;
        },
        updateBlackBoxName(state, value) {
            state.black_box.black_box_name = value;
        },
        updateSavedBoxes(state, value) {
            state.saved_black_boxes = value;
        }
    },
    getters: {
        black_box_active_half(state) {
            return state.black_box.active_half;
        },
        black_box_load_data(state) {
            return {
                lot_cost: state.black_box.lot_cost,
                loyalty: state.black_box.loyalty,
                rentability: state.black_box.rentability,
                costly_amount: state.black_box.costly_amount,
            }
        },
        black_box_input_data(state) {
            return {
                lot_cost: state.black_box.lot_cost,
                loyalty: state.black_box.loyalty,
                rentability: state.black_box.rentability,
                costly_amount: state.black_box.costly_amount,
                black_box_cost: state.black_box.black_box_cost.cur !== '' ? state.black_box.black_box_cost.cur : 0,
            }
        },
        black_box_output_data(state) {
            return {
                probabilities: state.black_box.probabilities,
                amounts: state.black_box.amounts,
                black_box_cost: state.black_box.black_box_cost,
            }
        },
        black_box_recalculate_data(state) {
            return {
                loyalty: state.black_box.loyalty,
                rentability: state.black_box.rentability,
                black_box_cost: state.black_box.black_box_cost,
                message: state.black_box.message,
            }
        },
        black_box_save_data(state) {
            return {
                name: state.black_box.black_box_name,
                price: state.black_box.black_box_cost.cur,
                lot_cost: state.black_box.lot_cost,
                lot_amount: state.black_box.amounts,
                //loyalty: state.black_box.loyalty,
                //rentability: state.black_box.rentability,
            }
        },
        saved_boxes(state) {
            return state.saved_black_boxes
        }
    },
    actions: {
        blackBoxReset(ctx) {
            ctx.commit('resetBlackBox')
        },
        async blackBoxCalculateParametersClicked(ctx,  form_input_data) {
            ctx.commit('updateBlackBoxInput', form_input_data)
            await this.dispatch('blackBoxSendCalculateRequest', ctx)
            ctx.commit('updateBlackBoxActiveHalf', 'bottom')
        },
        async blackBoxRecalculateParametersClicked(ctx,  form_recalc_data) {
            ctx.commit('updateBlackBoxRecalc', form_recalc_data)
            await this.dispatch('blackBoxSendCalculateRequest', ctx)
        },
        async blackBoxSendCalculateRequest(ctx) {
            ctx.commit('changeLoading', true)
            const url = `${ctx.getters.base_url}/black-box/calculate/`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ctx.getters.black_box_input_data)
            });
            if (response.ok) {
                const json = await response.json();
                ctx.commit('updateBlackBoxOutput', json)
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
            ctx.commit('changeLoading', false)
        },
        async saveBlackBox(ctx, name) {
            ctx.commit('changeLoading', true)
            ctx.commit('updateBlackBoxName', name)
            const url = `${ctx.getters.base_url}/black-box/`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ctx.getters.black_box_save_data)
            });
            if (response.ok) {
                ctx.dispatch('blackBoxReset')
                ctx.dispatch('loadBlackBoxes')
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
            ctx.commit('changeLoading', false)
        },
        async loadBlackBoxes(ctx) {
            ctx.commit('changeLoading', true)
            const url = `${ctx.getters.base_url}/black-box/`;
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            });
            if (response.ok) {
                const json = await response.json();
                ctx.commit('updateSavedBoxes', json)
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
            ctx.commit('changeLoading', false)
        },
        async deleteBlackBox(ctx, id) {
            ctx.commit('changeLoading', true)
            const url = `${ctx.getters.base_url}/black-box/${id}`;
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            });
            if (response.ok) {
                ctx.dispatch('loadBlackBoxes')
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
            ctx.commit('changeLoading', false)
        }
    }
}