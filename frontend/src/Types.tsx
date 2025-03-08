export interface loginParamsType {
    isAuthenticated : boolean,
    token : string,
    handleLogin : (loginToken: string) => void,
    handleLogout : () => void,
}

export type ProfileType = {
    id : number,
    username : string,
    email : string,
} | null

export type GroupMember = {
    id: number,
    username: string,
    email: string,
}

export type Expense = {
    id: number,
    name: string,
    amount: number,
    currency: string,
    payee: string,
    creation_date: string
}


export type Balances = Record<number, Record<number, Record<string, number>>>