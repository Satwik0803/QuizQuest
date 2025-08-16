import { Link } from 'react-router-dom';
import { useEffect } from 'react';

function Reset() {
    useEffect(() => {
        document.body.classList.add('login-body');

        return () => {
            document.body.classList.remove('login-body');
        };
    }, []);

    return(
        <div className = "login-window">
            <h2 className = "heading">Reset Password</h2>
            <div className = "underline-heading"></div>
            <div className = "credentials">
                <h3 className = "credentials-text">Username</h3>
                <div className = "input"><input type = "text"></input></div>
                <div className = "underline-credentials"></div>
                <h3 className = "credentials-text">New Password</h3>
                <div className = "input"><input type = "password"></input></div>
                <div className = "underline-credentials"></div>
                <h3 className = "credentials-text">Retype Password</h3>
                <div className = "input"><input type = "password"></input></div>
                <div className = "underline-credentials"></div>
            </div>
            <div className = "button">
                <Link to = "/">UPDATE</Link>
            </div>
        </div>
    );
}

export default Reset