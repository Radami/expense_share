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
    creation_date: string,
    you_owe: number,
}


export type BalancesType = Record<number, Record<number, Record<string, number>>>

export type MinimizedDebtType = {
    from_user: number,
    to_user: number,
    currency: string,
    amount: number,
}

export type FriendBalanceEntry = {
    currency: string;
    amount: number;
}

export type FriendGroupEntry = {
    id: number;
    name: string;
    you_owe: FriendBalanceEntry[];
    owed_to: FriendBalanceEntry[];
}

export type FriendType = {
    id: number;
    username: string;
    email: string;
    net: FriendBalanceEntry[];  // positive amount = they owe you, negative = you owe them
    groups: FriendGroupEntry[];
}

export type GroupType = {
    id: string,
    name: string,
    description: string,
    creation_date: string,
    group_members: GroupMemberType[],
    expenses: ExpenseType[],
    totals: Record<string, number>,
    balances: BalancesType,
    minimized_balances: MinimizedDebtType[],
    minimize_balances_setting: boolean,
    user_is_owed: string,
    user_owes: string,
}