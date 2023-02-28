import { useRouter } from 'next/router';
// import { useSelector } from 'react-redux';
import User from '../components/User'

const withAuth = (WrappedComponent) => {
    return (props) => {
        if (typeof window !== 'undefined') {
            const router = useRouter();

            const my_user: User = JSON.parse(localStorage.getItem('state_user'));

            console.dir(my_user);

            if (my_user === null || my_user.access_token === null || my_user.access_token.length === 0) {
                router.replace('/');
                return null;
            }

            return <WrappedComponent {...props} />;
        }
        return null;
    };
};

export default withAuth;