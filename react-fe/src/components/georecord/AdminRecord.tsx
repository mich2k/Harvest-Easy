import { useState, useEffect } from "react";
import React from "react";
import User from "../User";
import PersonList from "../PersonList";
import { Person } from "../PersonList";


import { useLocation } from "react-router-dom";
const AdminRecord = () => {
  const [user_firstname, setUserFistName] = useState<string>("Loading");
  const [apartment_name, setApartmentName] = useState<string>("Loading");
  const [today_date, setTodayDate] = useState<string>("default_user");

  const [people, setPeople] = useState<Person[]>([]);

  const handlePeopleChange = (people: Person[]) => {
    setPeople(people);
  };

  const { state } = useLocation();

  const user = state as User;


  useEffect(() => {
    console.log("useEffect");




  }, []);

  return (
    <div>
      <section className="h-full gradient-form bg-blue-100 md:h-screen">
        <div className="container py-12 px-6 h-full">
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
                          Welcome
                        </h4>
                      </div>
                    </div>
                    <h3 className="ml-4 text-xl font-semibold mt-2 pt-3 mb-4 pb-1">First-time apartment registration</h3>

                    <PersonList onPeopleChange={handlePeopleChange} ></PersonList>
                    <div>
                      <div className="m-4 mb-4 mt-16">Cosa permette di fare questo tool? Spiegaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</div>

                      <div className="text-center pt-1 mb-12 pb-1">
                        <button className="inline-block px-6 py-2.5 text-gray font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-400 hover:shadow-lg focus:shadow-lg focus:outline-none focus:ring-0 active:shadow-lg transition duration-150 ease-in-out w-full mb-3" type="button" data-mdb-ripple="true" data-mdb-ripple-color="light">
                          Register Apartment
                        </button>

                        {/* <a className="text-gray-500" href="#!">Tutto apposto?</a>
                                            
*/}
                      </div>
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

export default AdminRecord;
