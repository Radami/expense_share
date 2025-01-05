
function Friends({loginParams}) {



    return (
        <>
            <div className="container col-lg-4 mt-3">
            {loginParams.isAuthenticated ? ( 
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