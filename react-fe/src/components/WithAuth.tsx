import { useRouter } from 'next/router';
// import { useSelector } from 'react-redux';
import User from '../components/User'
import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { stat } from 'fs';





const withAuth = (WrappedComponent) => {


    return (props) => {
        if (typeof window !== 'undefined') {
            const localst_key = "authcmp_user";
            const router = useRouter();
            let state_user: User;

            if (router.query[0] !== undefined && Object.keys(router.query)[0].length > 0) {
                state_user = JSON.parse(Object.keys(router.query)[0]);
                localStorage.setItem(localst_key, JSON.stringify(state_user));
                console.log("p2d");

            }
            else {


                if (localStorage.getItem(localst_key) != null) {
                    state_user = JSON.parse(localStorage.getItem(localst_key));
                    console.log("p1d");

                } else {
                    console.log("pd");
                    router.replace('/');
                    return null;
                }


            }

            return <WrappedComponent user={state_user} />;
        }
        return null;
    };
};



withAuth.propTypes = {
    user: User
}


export default withAuth;