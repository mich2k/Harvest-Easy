import { useRouter } from 'next/router';
// import { useSelector } from 'react-redux';
import User from '../components/User'
import { useEffect, useState } from 'react';





const withAuth = (WrappedComponent) => {


    return (props) => {
        if (typeof window !== 'undefined') {

            const router = useRouter();
            console.log("param" + router.query);
            let state_user: User = JSON.parse(Object.keys(router.query)[0]);
            
            console.dir(state_user);


            if (state_user === null || state_user.access_token === null || state_user.access_token.length === 0) {
                router.replace('/');
                return null;
            }

            return <WrappedComponent {...props} />;
        }
        return null;
    };
};

export default withAuth;