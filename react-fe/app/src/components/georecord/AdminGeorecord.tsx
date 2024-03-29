import { useState, useEffect } from 'react'

import Error from '../Error'
import ErrorAlert from '../ErrorAlert';
import GenericError from '../GenericError'
import ReactLoading from 'react-loading';
import axios from 'axios'
import React from 'react';
import Coordinates from '../Coordinates';
import { useSearchParams, useNavigate } from 'react-router-dom';

const AdminGeorecord = () => {



    const APARTMENT_KEY_QUERY = 'ap_id';

    const [apartment_id, setApartmentId] = useState<string>('');
    const [checked_state, setCheck] = useState<boolean>(false);
    const [show_alert, setShowAlert] = useState<boolean>(false);
    const [isLoading, setLoading] = useState<boolean>(false);
    const [isGeoAllowanceGiven, setGeoAllowanceGiven] = useState<boolean>(false);
    const [deviceGeoCoordinates, setGeoCoordinates] = useState<Coordinates>();

    const [searchParams] = useSearchParams();

    const navigate = useNavigate();

    const [admin_username, setUsername] = useState<string>('');
    const [admin_password, setPassword] = useState<string>('');




    const [isGeoSupported, setGeoSupported] = useState<boolean>(true);


    const url = "https://flask.gmichele.it";

    useEffect(() => {
        document.title = "Admin Georecord";
    }, [])



    useEffect(() => {
        setLoading(true);
        if (isGeoAllowanceGiven) {
            setLoading(false);
        }


    }, [isGeoAllowanceGiven]);



    useEffect(() => {


        const ap_id = String(searchParams.get(APARTMENT_KEY_QUERY));

        setApartmentId(ap_id);

    }, []);


    useEffect(() => {

        if (!navigator.geolocation) {
            setGeoSupported(false);
            return;
        }

        navigator.geolocation.getCurrentPosition(function (position) {
            setGeoCoordinates(new Coordinates(position.coords.latitude, position.coords.longitude));
            setGeoAllowanceGiven(true);
        }, function (error) {
            if (error.code == error.PERMISSION_DENIED) {
                console.log("permission denied");
                setGeoAllowanceGiven(false);
            }
        });
    })


    const onLogInButtonClick = () => {

        if (!checked_state) {
            //console.log('check');
            setShowAlert(true);
            return;
        }



        const data = {
            username: admin_username,
            password: admin_password
        }


        axios
            .post(url + '/login/loginadmin', data, {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json;charset=UTF-8",
                },
            })
            .then(({ data }) => {
                //console.log(data);
                if (data['access_token'] === undefined) {
                    return <Error header_message="Invalid credentials" body_message="The credentials you have entered are not valid, please try again"></Error>
                } else {
                    navigate("/admin_home", {
                        state: { coords: deviceGeoCoordinates, access_token: data['access_token'], admin_username: admin_username, apartment_id: apartment_id },
                    });
                }

            });




    }


    if (!isGeoSupported) {
        return <GenericError current_path={"test"} body_message={"Your device does not support geo-location, please change device to proceed."}></GenericError>

    } else {


        if (isLoading) {
            return (
                <section className="grid h-screen place-items-center">
                    <span className='grid justify-items'></span>
                    <span className='grid justify-items'></span>
                    <ReactLoading type={"cylon"} color={"gray"} height={"10%"} width={"10%"} />
                    Loading...
                    <span className='grid justify-items'></span>
                    <span className='grid justify-items'></span>
                    <span className='grid justify-items'></span>
                </section >
            );
        }
        else {
            if (apartment_id === undefined || apartment_id === null || apartment_id === "") {
                return <Error
                    header_message="Apartment ID invalid or not specified or a broken QR Code"
                ></Error>;
            } else {
                if (!isGeoAllowanceGiven || deviceGeoCoordinates === undefined) {
                    return <GenericError current_path={"test"} body_message={"Has not been possible to retrieve geo coordinates from your device, please give geolocation allowance from the settings in your browser or will not be possible to proceed to apartment registration"}></GenericError>
                }
                if (isGeoAllowanceGiven && deviceGeoCoordinates !== undefined && !isLoading) {
                    return (

                        <section className="h-full gradient-form bg-gray-200 md:h-screen">
                            <div className="container py-12 px-6 h-full">
                                <div className="flex justify-center items-center flex-wrap h-full g-6 text-gray-800">
                                    <div className="xl:w-10/12">
                                        <div className="block bg-white shadow-lg rounded-lg">
                                            <div className="lg:flex lg:flex-wrap g-0">
                                                <div className="lg:w-6/12 px-4 md:px-0">
                                                    <div className="md:p-12 md:mx-6">
                                                        <div className="text-center">
                                                            <img
                                                                className="mx-auto w-48"
                                                                width="100px"
                                                                src="https://hero.gmichele.it/HE-Logo.jpg"
                                                                alt="logo"
                                                            />
                                                            <h4 className="text-xl font-semibold mt-1 mb-8 pb-1">Apartment registration tool</h4>
                                                            <h5 className="text-l font-italic mt-1 mb-4 pb-1">You are trying to initialize the following apartment: </h5>
                                                            <div>
                                                                <span className="font-bold">Apartment ID:</span> <span>{apartment_id}</span>
                                                            </div>
                                                            <div>
                                                                <span className="font-bold">Your Coordinates:</span>

                                                                <span>LA: {deviceGeoCoordinates.toStringCoordinates()[0]}, LO: {deviceGeoCoordinates.toStringCoordinates()[1]}</span>
                                                            </div>
                                                            <div>

                                                            </div>

                                                        </div>
                                                        <form>
                                                            <p className="mb-4 mt-4">Please access with given credentials</p>
                                                            <div className="mb-4">
                                                                <input
                                                                    type="text"
                                                                    className="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                                                                    id="admin_username_textinput"
                                                                    placeholder="Admin username"
                                                                    onChange={(e) => { setUsername(e.target.value) }}
                                                                />
                                                            </div>
                                                            <div className="mb-4">
                                                                <input
                                                                    type="password"
                                                                    className="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                                                                    id="admin_password_textinput"
                                                                    placeholder="Master password"
                                                                    onChange={(e) => { setPassword(e.target.value) }}

                                                                />
                                                            </div>
                                                            <div className="text-center pt-1 mb-12 pb-1">
                                                                <button
                                                                    className="inline-block px-6 py-2.5 text-gray font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-400 hover:shadow-lg focus:shadow-lg focus:outline-none focus:ring-0 active:shadow-lg transition duration-150 ease-in-out w-full mb-3"
                                                                    type="button"
                                                                    data-mdb-ripple="true"
                                                                    data-mdb-ripple-color="light"
                                                                    onClick={onLogInButtonClick}
                                                                >
                                                                    Log in
                                                                </button>
                                                                <div className="flex items-center mb-2 mt-2">
                                                                    <input onChange={() => { setCheck(!checked_state); }} id="default-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
                                                                    <label htmlFor="default-checkbox" className="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Confirm apartment id</label>
                                                                </div>
                                                            </div>
                                                            <div id="alert"> {show_alert ? <ErrorAlert alert_type={'warn'} body_message={"Please confirm by checking the checkbox in order to confirm you want to init this apartment"}></ErrorAlert> : null} </div>

                                                        </form>
                                                    </div>
                                                </div>
                                                <div
                                                    className="lg:w-6/12 flex items-center lg:rounded-r-lg rounded-b-lg lg:rounded-bl-none"
                                                >
                                                    <div className="text-black px-4 py-6 md:p-12 md:mx-6">
                                                        <h4 className="text-xl font-semibold mb-6">We are more than just a bin, let me explain y.</h4>
                                                        <p className="text-sm">
                                                            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                                                            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                                                            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                                                            consequat.
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>
                    )
                }
            }
        }
    }
}

export default AdminGeorecord;
