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