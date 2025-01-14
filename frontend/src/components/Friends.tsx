import { LoginParamsType } from '../Types';

interface FriendsProps {
    login_params: LoginParamsType,
}

const Friends: React.FC<FriendsProps> = ({ login_params }) => {
    return (
        <>
            <div className="container col-lg-4 mt-3">
            {login_params.isAuthenticated ? ( 
                <p>Friends</p>
            ) : (
                <p>
                    Please log in
                </p>
            )
            }
            </div>
        </>
   );

}

export default Friends;