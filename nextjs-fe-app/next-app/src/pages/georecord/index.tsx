import type { NextPage } from 'next'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'

import Error from '../../components/Error'
import ErrorAlert from '../../components/ErrorAlert'
import GenericError from '../../components/GenericError'
import ReactLoading from 'react-loading';
import axios from 'axios'

const Home: NextPage = () => {

    const APARTMENT_KEY_QUERY = 'ap_id';

    const [apartment_id, setApartmentId] = useState<string>('');
    const [checked_state, setCheck] = useState<boolean>(false);
    const [show_alert, setShowAlert] = useState<boolean>(false);
    const [isLoading, setLoading] = useState<boolean>(false);
    const [isGeoAllowanceGiven, setGeoAllowanceGiven] = useState<boolean>(false);
    const [data, setData] = useState(null);
    const [deviceGeoCoordinates, setGeoCoordinates] = useState<{ lat: number, lon: number }>({ "lat": undefined, "lon": undefined });

    const [user, setUser] = useState({ username: '', access_token: '', birth_year: 1900, name: '', last_name: '', city: '', apartment_id: '' });


    const router = useRouter();


    const [isGeoSupported, setGeoSupported] = useState<boolean>(true);


    const url = "https://flask.gmichele.it";



    useEffect(() => {
        setLoading(true);
        if (isGeoAllowanceGiven) {
            setLoading(false);
        }


    }, [isGeoAllowanceGiven]);

    useEffect(() => {
        import("flowbite/dist/flowbite");
    }, []);

    useEffect(() => {
        setApartmentId(String(router.query[APARTMENT_KEY_QUERY]))
    }, [String(router.query[APARTMENT_KEY_QUERY])])


    useEffect(() => {

        if (!navigator.geolocation) {
            setGeoSupported(false);
            return;
        }

        navigator.geolocation.getCurrentPosition(function (position) {
            setGeoCoordinates({ lat: position.coords.latitude, lon: position.coords.longitude });
            setGeoAllowanceGiven(true);
            // console.log("Latitude is :", position.coords.latitude);
            // console.log("Longitude is :", position.coords.longitude);
        }, function (error) {
            if (error.code == error.PERMISSION_DENIED) {
                console.log("permission denied");
                setGeoAllowanceGiven(false);
            }
        });
    })


    /*
    useEffect(() => {
        setLoading(true)
        fetch('https://flask.gmichele.it/getBins/Modena')
            .then((res) => res.json())
            .then((data) => {
                setData(data)
                setLoading(false)
            })
    }, [])

    */



    const onLogInButtonClick = () => {
        console.log(checked_state);

        if (!checked_state) {
            console.log('check');
            setShowAlert(true);
            return;
        }


        const data = {
            username: 'rossi1',
            password: 'mariorossi'
        }


        axios
            .post(url + '/login/loginadmin', data, {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json;charset=UTF-8",
                },
            })
            .then(({ data }) => {
                console.log(data);
            });

    }


    if (!isGeoSupported) {
        return <GenericError current_path={router.asPath} body_message={"Your device does not support geo-location, please change device to proceed."}></GenericError>

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
            if (Object.keys(router.query).length === 0
                || !(APARTMENT_KEY_QUERY in router.query)
                || router.query[APARTMENT_KEY_QUERY].length === 0) {
                return <Error
                    header_message="Apartment ID invalid or not specified or a broken QR Code"
                ></Error>;
            } else {
                if (!isGeoAllowanceGiven || deviceGeoCoordinates['lat'] === undefined || deviceGeoCoordinates['lon'] === undefined) {
                    return <GenericError current_path={router.asPath} body_message={"Has not been possible to retrieve geo coordinates from your device, please give geolocation allowance from the settings in your browser or will not be possible to proceed to apartment registration"}></GenericError>
                }
                if (isGeoAllowanceGiven && deviceGeoCoordinates['lat'] !== undefined && deviceGeoCoordinates['lon'] !== undefined && !isLoading) {
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
                                                                src="https://e7.pngegg.com/pngimages/165/760/png-clipart-s-s-c-napoli-2017-audi-cup-stadio-san-paolo-football-uefa-champions-league-football-ssc-napoli-2017-audi-cup.png"
                                                                alt="logo"
                                                            />
                                                            <h4 className="text-xl font-semibold mt-1 mb-8 pb-1">Apartment registration tool</h4>
                                                            <h5 className="text-l font-italic mt-1 mb-4 pb-1">You are trying to initialize the following apartment: </h5>
                                                            <p>
                                                                <span className="font-bold">Apartment ID:</span> <span>{apartment_id}</span>
                                                            </p>
                                                            <p>
                                                                <span className="font-bold">Your Coordinates:</span> <span>[LA: {deviceGeoCoordinates.lat}, LO: {deviceGeoCoordinates.lon}]</span>
                                                            </p>
                                                            <p>
                                                                <span className="font-bold">Detected geo-reversed city:</span> <span>{apartment_id}</span>
                                                            </p>

                                                        </div>
                                                        <form>
                                                            <p className="mb-4 mt-4">Please access with given credentials</p>
                                                            <div className="mb-4">
                                                                <input
                                                                    type="text"
                                                                    className="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                                                                    id="exampleFormControlInput1"
                                                                    placeholder="Admin username"
                                                                />
                                                            </div>
                                                            <div className="mb-4">
                                                                <input
                                                                    type="password"
                                                                    className="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                                                                    id="exampleFormControlInput2"
                                                                    placeholder="Master password"
                                                                />
                                                            </div>
                                                            {data}
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
                                                                <div className="flex items-center mb-4">
                                                                    <input onChange={() => { setCheck(!checked_state); }} id="default-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
                                                                    <label htmlFor="default-checkbox" className="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Confirm apartment id</label>
                                                                </div>
                                                                <a className="text-gray-500" href="#!">Valuta funzione da inserire</a>
                                                            </div>
                                                            <div id="alert"> {show_alert ? <ErrorAlert alert_type={'warn'} body_message={"Please confirm by checking the checkbox in order to confirm you want to init this apartment"}></ErrorAlert> : null} </div>

                                                            { /** 
                    <div className="flex items-center justify-between pb-6">
                      <p className="mb-0 mr-2">Don't have an account?</p>
                      <button
                        type="button"
                        className="inline-block px-6 py-2 border-2 border-red-600 text-red-600 font-medium text-xs leading-tight uppercase rounded hover:bg-black hover:bg-opacity-5 focus:outline-none focus:ring-0 transition duration-150 ease-in-out"
                        data-mdb-ripple="true"
                        data-mdb-ripple-color="light"
                      >
                        Danger
                      </button>
                    </div>
                  */ }

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

                                                            Spiega che roba è.

                                                            Bidone fantastico bellissimo me lo sposo guarda eccomi ciao.
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

export default Home
