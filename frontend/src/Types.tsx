export interface LoginParamsType {
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

export type GroupMemberType = {
    id: number,
    username: string,
    email: string,
}

export type ExpenseType = {
    id: string,
    name: string,
    amount: number,
    currency: string,
    payee: string,
    creation_date: string
}


export type BalancesType = Record<number, Record<number, Record<string, number>>>

export type GroupType = {
    id: string,
    name: string,
    description: string,
    creation_date: string,
    group_members: GroupMemberType[],
    expenses: ExpenseType[],
    totals: Record<string, number>,
    balances: BalancesType,
}