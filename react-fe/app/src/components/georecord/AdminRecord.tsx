import { useState, useEffect } from "react";
import React from "react";
import PersonList from "../PersonList";
import { Person } from "../PersonList";
import { useLocation } from "react-router-dom";
import Coordinates from "../Coordinates";
import GenericError from "../GenericError";
import ErrorAlert from "../ErrorAlert";
import axios from "axios";

class toSendMsg {
  timestamp: string;
  apartment_name: string;
  common_city: string;
  admin_username: string;
  apartment_coords: Coordinates;
  final_people: Person[];
  apartment_waste_sorting: string[];

  constructor(final_people: Person[], apartment_waste_sorting: string[], common_city: string, apartment_name: string, timestamp: string, admin_username: string, apartment_coords: Coordinates) {
    this.final_people = final_people;
    this.apartment_waste_sorting = apartment_waste_sorting;
    this.common_city = common_city;
    this.apartment_name = apartment_name;
    this.timestamp = timestamp;
    this.admin_username = admin_username;
    this.apartment_coords = apartment_coords;
  }
}




const AdminRecord = () => {
  const [cmn_city, setCommonCity] = useState<string>("Unknown");
  const [apartment_id, setApartmentId] = useState<string>('');
  const [auth_token, setAuthToken] = useState<string>("default_token");

  const [people, setPeople] = useState<Person[]>([]);
  const [apartment_coords, setApartmentCoords] = useState<Coordinates>();
  const [admin_username, setUsername] = useState<string>('');

  const [apartment_waste_sorting, setApartmentWasteSorting] = useState<Set<string>>(new Set());

  const handlePeopleChange = (people: Person[]) => {
    setPeople(people);
  };
  const { state } = useLocation();


  useEffect(() => {
    if (!state) {
      return;
    }
    setApartmentCoords(state["coords"]);
    setUsername(state["admin_username"]);
    setApartmentId(state["apartment_id"]);
    setAuthToken(state["access_token"]);
  }, [state])



  const onCheckboxChange = (type: string) => {

    const newApartmentWasteSorting = new Set(apartment_waste_sorting);
    if (newApartmentWasteSorting.has(type)) {
      newApartmentWasteSorting.delete(type);
    } else {
      newApartmentWasteSorting.add(type);
    }
    setApartmentWasteSorting(newApartmentWasteSorting);

    console.dir(newApartmentWasteSorting);

  }

  const onApartmentRegister = () => {

    if (Array.from(apartment_waste_sorting).length == 0 || people.length == 0) {

      alert("Please add at least one user or specify apartment waste sorting type(s)");

      return;
    }



    if (cmn_city == "Unknown") {
      alert("Please specify the city where the apartment is located");
      return;

    }

    const url = "https://flask.gmichele.it";

    const msg = new toSendMsg(people, Array.from(apartment_waste_sorting), cmn_city, apartment_id, new Date().toISOString(), admin_username, apartment_coords as Coordinates);

    console.dir(msg);


    axios
      .post(url + '/login/ApartmentInit', msg, {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json;charset=UTF-8",
          Authorization: "Bearer " + auth_token,
        },
      })
      .then(({ data }) => {

        console.dir(data);




      });
  }

  if (!apartment_coords || !admin_username || !apartment_id) {

    return <GenericError current_path={"/"} body_message={"Missing URL parameters, did you go through login?"}></GenericError>



  }
  else {
    return (
      <div>
        <section className="h-full gradient-form bg-blue-100 md:h-screen overflow-auto	">
          <div className="container pl-5 py-12 h-full">
            <div className="flex justify-center items-center flex-wrap h-full g-6 text-gray-800">
              <div className="xl:w-10/12">
                <div className="block bg-white shadow-lg rounded-lg">
                  <div className="lg:flex lg:flex-wrap g-0">
                    <div className="lg:w-6/12 px-4 md:px-0">
                      <div className="md:p-12 md:mx-6">
                        <div className="text-left">
                          <h3 className="text-xl font-semibold ml-4 mt-2 pt-3 mb-0 pb-1">Apartment &quot;{apartment_id}&quot;</h3>

                          <h4 className="text-xl ml-4 font-semibold mt-1 mb-0 pb-1">
                            Welcome
                          </h4>
                        </div>
                      </div>
                      <h3 className="ml-4 text-xl font-semibold mt-2 pt-3 mb-4 pb-1">First-time apartment registration tool</h3>
                      <div className="ml-4">
                        <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                          Apartment City:
                          <input
                            type="text"
                            className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                            value={cmn_city}
                            onChange={(e) => setCommonCity(e.target.value)}
                          />
                        </label>
                      </div>

                      <PersonList onPeopleChange={handlePeopleChange} ></PersonList>

                      <hr className="mt-4 mb-4"></hr>

                      <div className="ml-4">
                        <h2 className="mb-4 font-semibold text-gray-900 dark:text-white">Check which materials the condominium separates</h2>
                        <ul className="w-48 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                          <li className="w-full border-b border-gray-200 rounded-t-lg dark:border-gray-600">
                            <div className="flex items-center pl-3">
                              <input onChange={() => { onCheckboxChange("paper") }} id="paper-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />
                              <label htmlFor="paper-checkbox" className="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Paper</label>
                            </div>
                          </li>
                          <li className="w-full border-b border-gray-200 rounded-t-lg dark:border-gray-600">
                            <div className="flex items-center pl-3">
                              <input onChange={() => { onCheckboxChange("plastic") }} id="plastic-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />
                              <label htmlFor="plastic-checkbox" className="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Plastic</label>
                            </div>
                          </li>
                          <li className="w-full border-b border-gray-200 rounded-t-lg dark:border-gray-600">
                            <div className="flex items-center pl-3">
                              <input onChange={() => { onCheckboxChange("glass") }} id="glass-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />
                              <label htmlFor="glass-checkbox" className="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Glass</label>
                            </div>
                          </li>
                          <li className="w-full border-b border-gray-200 rounded-t-lg dark:border-gray-600">
                            <div className="flex items-center pl-3">
                              <input onChange={() => { onCheckboxChange("organic") }} id="organic-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />
                              <label htmlFor="organic-checkbox" className="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Organic</label>
                            </div>
                          </li>
                        </ul>
                      </div>
                      <hr className="mt-6 mb-1"></hr>




                      <div>
                        <div className="m-4 mb-4 mt-16">Fill all the req. fields & press Register, in this way the apartment and the users will be created.</div>

                        <div className="text-center pt-1 mb-12 pb-1">
                          <button onClick={onApartmentRegister} className="inline-block px-6 py-2.5 text-gray font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-400 hover:shadow-lg focus:shadow-lg focus:outline-none focus:ring-0 active:shadow-lg transition duration-150 ease-in-out w-full mb-3" type="button" data-mdb-ripple="true" data-mdb-ripple-color="light">
                            Register Apartment
                          </button>
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
  }
};

export default AdminRecord;
