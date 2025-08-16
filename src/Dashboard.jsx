import { Link } from 'react-router-dom';
import home from './assets/home.svg';
import results from './assets/results.svg';
import signout from './assets/sign-out.svg';
import python from './assets/python.svg';
import cpp from './assets/c++.svg';
import java from './assets/java.svg';

function Dashboard () {
    return (
        <>
            <header className = "sidebar">
                <Link to = "/dashboard" className='logo'>QuizQuest</Link>
                <div className="sidebar-buttons">
                    <Link to = "/dashboard">
                        <img src = {home}></img>
                        Home
                    </Link>

                    <Link to = "/results">
                        <img src = {results}></img>
                        Results
                    </Link>

                    <Link to = "/" className="sidebar-bottom">
                        <img src = {signout}></img>
                        Sign Out
                    </Link>
                </div>
            </header>

            <main className="dashboard-results-main-content">
                <h1 className="page-title">Home</h1>
                <h2 className="page-subheading">Welcome, User!</h2>
                
                <div className = "dashboard-results-sections">
                    <div className = "left-section">
                        <div className = "courses-or-results-container">
                            <h2 className = "courses-scores-title">Courses</h2>
                            <div className = "card-container">
                                <Link to = '/python' className = "course-or-score-card">
                                    <div className = "course-card-logo">
                                        <img src = {python}></img>
                                    </div>
                                <h2 className = "course-title">Python</h2>
                                </Link>

                                <Link to = '/cpp' className = "course-or-score-card">
                                    <div className = "course-card-logo">
                                        <img src = {cpp}></img>
                                    </div>
                                    <h2 className = "course-title">C++</h2>
                                </Link>

                                <Link to = '/java' className = "course-or-score-card">
                                    <div className = "course-card-logo">
                                        <img src = {java}></img>
                                    </div>
                                    <h2 className = "course-title">Java</h2>
                                </Link>
                            </div>
                        </div>

                        <div className = "result-summary">
                            <h2 className = "summary-title">Result Summary</h2>
                            <ul className = "summary-info">
                                <li>Quizzes Attempted: 0</li>
                                <li>Average Score: 0%</li>
                            </ul>
                            <h2 className = "feedback">Feedback: Attempt quizzes for feedback.</h2>
                        </div>
                    </div>

                    <div className = "quizzes-attempted">
                        <h2 className = "attempts-title">Quizzes Attempted</h2>

                        <div className = "attempt-card">
                            <div className = "attempt-card-title">
                                <h2>Python</h2>
                            </div>

                            <p className = "attempt-info">Total Quizzes: 2</p>
                            <p className = "attempt-info">Attempted: 0</p>
                        </div>

                        <div className = "attempt-card">
                            <div className = "attempt-card-title">
                                <h2>C++</h2>
                            </div>

                            <p className = "attempt-info">Total Quizzes: 2</p>
                            <p className = "attempt-info">Attempted: 0</p>
                        </div>

                        <div className = "attempt-card">
                            <div className = "attempt-card-title">
                                <h2>Java</h2>
                            </div>

                            <p className = "attempt-info">Total Quizzes: 2</p>
                            <p className = "attempt-info">Attempted: 0</p>
                        </div>
                    </div>
                </div>
            </main>
        </>
    );
}

export default Dashboard