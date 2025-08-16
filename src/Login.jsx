import { Link } from 'react-router-dom';
import { useEffect } from 'react';

function Login() {
    useEffect(() => {
        document.body.classList.add('login-body');

        return () => {
            document.body.classList.remove('login-body');
        };
    }, []);

    return(
            <div className = "login-window">
                <h2 className = "heading">Login</h2>
                <div className = "underline-heading"></div>
                <div className = "credentials">
                    <h3 className = "credentials-text">Username</h3>
                    <div className = "input"><input type = "text"></input></div>
                    <div className = "underline-credentials"></div>
                    <h3 className = "credentials-text">Password</h3>
                    <div className = "input"><input type = "password"></input></div>
                    <div className = "underline-credentials"></div>
                </div>
                <div className = "forgot-password">
                    <Link to="/reset">Forgot Password?</Link>
                </div>
                <div className = "button">
                    <Link to = "/create">SIGN-UP</Link>
                    <Link to = "/dashboard">LOGIN</Link>
                </div>
            </div>
    );
}

export default Login