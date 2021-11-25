const default_lottery = {
    active_half: 'top',
    lots: [{price:'', amount: ''}],
    write_off: '',
    referral_on: false,
    referral_coeff: '',
    discount: '',
    ticket_amount: {
        min: '',
        cur: '',
        max: ''
    },
    ticket_price: {
        min: '',
        cur: '',
        max: ''
    },
    total_cost: '',
    min_profit: '',
    min_rentability: '',
    max_rentability: '',
    message: '',
    name: '',
}

export default {
    state: {
        lottery: default_lottery,
        saved_lotteries: [],
    },
    mutations: {
        resetLottery(state) {
            state.lottery = default_lottery
        },
        updateLotteryInput(state, form_input_data) {
            state.lottery = {...state.lottery, ...form_input_data}
        },
        updateLotteryOutput(state, output_json) {
            state.lottery = {...state.lottery, ...output_json}
        },
        updateLotteryRecalc(state, form_recalc_data) {
            state.lottery = {...state.lottery, ...form_recalc_data}
        },
        updateLotteryActiveHalf(state, value) {
            state.lottery.active_half = value;
        },
        updateLotteryName(state, value) {
            state.lottery.name = value;
        },
        updateSavedLotteries(state, value) {
            state.saved_lotteries = value;
        }
    },
    getters: {
        lottery_active_half(state) {
            return state.lottery.active_half;
        },
        lottery_load_data(state) {
            return {
                lots: state.lottery.lots,
                write_off: state.lottery.write_off,
                referral_on: state.lottery.referral_on,
                referral_coeff: state.referral_coeff,
                discount: state.discount,
            }
        },
        lottery_input_data(state) {
            return {
                lots: state.lottery.lots,
                write_off: state.lottery.write_off,
                referral_coeff: state.lottery.referral_on ? state.lottery.referral_coeff : 0,
                discount: state.lottery.referral_on ? state.lottery.discount : 0,
                ticket_price: state.lottery.ticket_price.cur !== '' ? state.lottery.ticket_price.cur : 0,
                ticket_amount: state.lottery.ticket_amount.cur !== '' ? state.lottery.ticket_amount.cur : 0,
            }
        },
        lottery_output_data(state) {
            return {
                ticket_amount: state.lottery.ticket_amount,
                total_cost: state.lottery.total_cost,
                ticket_price: state.lottery.ticket_price,
                min_profit: state.lottery.min_profit,
                write_off: state.lottery.write_off,
                min_rentability: state.lottery.min_rentability,
                max_rentability: state.lottery.max_rentability,
            }
        },
        lottery_recalc_data(state) {
            return {
                ticket_price: state.lottery.ticket_price,
                ticket_amount: state.lottery.ticket_amount,
                message: state.lottery.message,
            }
        },
        lottery_save_data(state) {
            return {
                name: state.lottery.name,
                lots: state.lottery.lots,
                write_off: state.lottery.write_off,
                referral_coeff: state.lottery.referral_coeff,
                ticket_amount: state.lottery.ticket_amount.cur,
                total_cost: state.lottery.total_cost,
                ticket_price: state.lottery.ticket_price.cur,
                min_profit: state.lottery.min_profit,
                min_rentability: state.lottery.min_rentability,
                max_rentability: state.lottery.max_rentability,
                discount: state.lottery.discount,
            }
        },
        saved_lotteries(state) {
            return state.saved_lotteries
        }
    },
    actions: {
        lotteryReset(ctx) {
            ctx.commit('resetLottery')
        },
        async lotteryCalculateParametersClicked(ctx,  form_input_data) {
            ctx.commit('updateLotteryInput', form_input_data)
            await this.dispatch('lotteryCalculateRequest', ctx)
            ctx.commit('updateLotteryActiveHalf', 'bottom')
        },
        async lotteryRecalculateParametersClicked(ctx,  form_recalc_data) {
            ctx.commit('updateLotteryRecalc', form_recalc_data)
            await this.dispatch('lotteryCalculateRequest', ctx)
        },
        async lotteryCalculateRequest(ctx) {
            ctx.commit('changeLoading', true)
            const url = `${ctx.getters.base_url}/lottery/calculate/`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ctx.getters.lottery_input_data)
            });
            if (response.ok) {
                const json = await response.json();
                ctx.commit('updateLotteryOutput', json)
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
            ctx.commit('changeLoading', false)
        },
        async loadLotteries(ctx) {
            ctx.commit('changeLoading', true)
            const url = `${ctx.getters.base_url}/lottery/`;
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            });
            if (response.ok) {
                const json = await response.json();
                ctx.commit('updateSavedLotteries', json)
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
            ctx.commit('changeLoading', false)
        },
        async saveLottery(ctx, name) {
            ctx.commit('changeLoading', true)
            ctx.commit('updateLotteryName', name)
            const url = `${ctx.getters.base_url}/lottery/`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ctx.getters.lottery_save_data)
            });
            if (response.ok) {
                ctx.dispatch('lotteryReset')
                ctx.dispatch('loadLotteries')
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
            ctx.commit('changeLoading', false)
        },
        async deleteLottery(ctx, id) {
            ctx.commit('changeLoading', true)
            const url = `${ctx.getters.base_url}/lottery/${id}`;
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            });
            if (response.ok) {
                ctx.dispatch('loadLotteries')
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
            ctx.commit('changeLoading', false)
        }
    }
}