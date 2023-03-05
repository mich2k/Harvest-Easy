import { useState, useEffect } from "react";
import React from "react";
import User from "../User";
import { Flowbite } from "flowbite-react";
import useToken from "../../useToken";

import { useLocation } from "react-router-dom";
const Home = () => {
  const [user_firstname, setUserFistName] = useState<string>("Loading");
  const [user_lastname, setUserLastName] = useState<string>("Loading");
  const [apartment_name, setApartmentName] = useState<string>("Loading");
  const [estimated_fill_date, setEstimatedFillDate] = useState<string>(new Date().toISOString().split(".")[0]);
  const [today_date, setTodayDate] = useState<string>("default_user");

  const [user_role, setUserRole] = useState<string>("default_user");

  const [state_user, setUser] = useState<User>();

  const {state} = useLocation();


  
  const user = state as User;


  useEffect(() => {
    console.log("useEffect");

    const localst_key = "home_user";
    const u = new User("default_user", "default_user", "default_user", "default_user", "default_user", "default_user", 0, "default_user", 0);
    u.fromObj(state["user"]);
    setUser(u);
    console.dir(state_user);


  }, []);

  return (
    <div>
      <section className="h-full gradient-form bg-blue-100 md:h-screen">
        <div className="container py-12 h-full">
          <div className="flex justify-center items-center flex-wrap h-full g-6 text-gray-800">
            <div className="xl:w-10/12">
              <div className="block bg-white shadow-lg rounded-lg">
                <div className="lg:flex lg:flex-wrap g-0">
                  <div className="lg:w-6/12 px-4 md:px-0">
                    <div className="md:p-12 md:mx-6">
                      <div className="text-left">
                        {/* <img
                                                className="mx-auto w-48"
                                                width="100px"
                                                src=""
                                                alt="logo"
    /> */}
                        <h3 className="text-xl font-semibold mt-2 pt-3 mb-0 pb-1">Apartment {apartment_name}.</h3>

                        <h4 className="text-xl font-semibold mt-1 mb-0 pb-1">
                          Welcome in your house dashboard {user_firstname} {user_lastname}.
                        </h4>
                        <h4 className="text-l font-semibold mt-1 mb-4 pb-1">Today is today , beautiful day, isn&apos;t it?</h4>
                      </div>
                    </div>
                    <h3 className="text-xl font-semibold mt-2 pt-3 mb-4 pb-1">Let me guess 🔮</h3>

                    <div className="w-full bg-gray-200 rounded-full dark:bg-gray-700">
                      <div className="bg-blue-600 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full" style={{ width: "69%" }}>
                        69%
                      </div>
                    </div>
                    <div className="text-right mt-4">Estimated filling:</div>
                    <div>
                      <div className="mb-4 mt-16">Lorem, ipsum dolor sit amet consectetur adipisicing elit. Rerum qui quibusdam, beatae ipsum labore voluptatibus ratione, itaque expedita neque natus consequuntur et culpa voluptatem odit ipsam excepturi accusantium cum laudantium consequatur tenetur necessitatibus velit amet eum optio? Quaerat porro, officia obcaecati excepturi natus quo fugit perferendis eveniet laborum, quas nostrum.</div>

                      <div className="text-center pt-1 mb-12 pb-1">
                        <button className="inline-block px-6 py-2.5 text-gray font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-400 hover:shadow-lg focus:shadow-lg focus:outline-none focus:ring-0 active:shadow-lg transition duration-150 ease-in-out w-full mb-3" type="button" data-mdb-ripple="true" data-mdb-ripple-color="light">
                          Log in
                        </button>

                        {/* <a className="text-gray-500" href="#!">Tutto apposto?</a>
                                            
*/}
                      </div>
                    </div>
                  </div>

                  <div className="lg:w-6/12 flex items-center lg:rounded-r-lg rounded-b-lg lg:rounded-bl-none">
                    <div className="text-black px-4 py-6 md:p-12 md:mx-6">
                      <h4 className="text-xl font-semibold mb-6">Right card.</h4>
                      <div className="text-sm">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Spiega che roba è. Bidone fantastico bellissimo me lo sposo guarda eccomi ciao.</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
