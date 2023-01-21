import axios, { AxiosResponse } from "axios";

export const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    withCredentials: true,
})


export const Api = {
    getData() {
        return instance.get<any, AxiosResponse<any>>('/api/index');
    },
    getTimeData(startDate: number, endDate: number) {
        return instance.get<any, AxiosResponse<any>>('/api/index' + '?DateFrom=' + startDate + "&DateTo=" + endDate);
    }
}

// http://127.0.0.1:8000/api/index?DateFrom=1674180724392&DateTo=1674180805000