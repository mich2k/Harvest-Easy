import { useState, useEffect } from "react";
import React from "react";
import User from "../User";
import { Collapse } from 'react-collapse';
import { FaMinus, FaPlus } from 'react-icons/fa';
import useToken from "../../useToken";
import { BinProphetRecord } from "../BinProphetRecord";
import { useLocation } from "react-router-dom";
import axios from "axios";
import Base64Image from "../Base64Img";

const Home = () => {


  type base64Prevision = {
    [key: string]: string
  };

  interface apartmentPrevisions {
    previsione_status: Date;  // ETA Filling date
    riempimento: number;    // Actual Filling percentage
    status: number;         // FSM status
    tipologia: "carta" | "plastica" | "vetro";
    // Type of waste, sorting type


  }


  const [user_firstname, setUserFistName] = useState<string>("Loading");
  const [user_lastname, setUserLastName] = useState<string>("Loading");
  const [apartment_name, setApartmentName] = useState<string>("Loading");
  const [estimated_fill_date, setEstimatedFillDate] = useState<string>(new Date().toISOString().split(".")[0]);
  const [today_date, setTodayDate] = useState<string>("default_user");

  const [user_role, setUserRole] = useState<string>("default_user");

  const [state_user, setUser] = useState<User>();
  const [isOpen, setIsOpen] = useState(false);

  const { state } = useLocation();

  const [datePrevision, setDatePrevision] = useState<apartmentPrevisions[] | undefined>([]);
  const [base64ChartPrevision, setbase64ChartPrevision] = useState<base64Prevision[] | undefined>([]);

  const url = "https://flask.gmichele.it";



  const weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  const typologyColorMap = { "vetro": "bg-green-600", "plastica": "bg-blue-600", "carta": "bg-yellow-300", "umido": "bg-orange-900", "other": "bg-black-600" };


  const type = "carta";

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  useEffect(() => {
    if (!state) {
      return;
    }
    console.dir(state);
  }, [state])

  useEffect(() => {

    const localst_key = "home_user";
    const u = new User("default_user", "default_user", "default_user", "default_user", "default_user", "default_user", 0, "default_user", 0);
    u.fromObj(state["user"]);
    setUser(u);
    console.dir(state_user);


  }, []);


  useEffect(() => {
    axios.get(url + "/get/urlprevision/" + state["apartment_name"], {
      headers: {
        Authorization: "Bearer " + state["access_token"]
      }
    }).then((response) => {
      const data = response.data;
      setbase64ChartPrevision(data);
      //console.dir(data);
      console.dir(base64ChartPrevision);

    }).catch((error) => {
      console.log(error);
    });
  }, [state]);


  useEffect(() => {
    console.log(state["apartment_name"]);
    async () => {
      await axios.get(url + "/get/prevision/" + state["apartment_name"], {
        headers: {
          Authorization: "Bearer " + state["access_token"]
        }
      }).then((response) => {
        const data = response.data;
        setDatePrevision(data);
        console.dir(datePrevision);
      }).catch((error) => {
        console.log(error);
      });
    }
  }, [state]);


  const iteratate64ToImg = () => {
    if (base64ChartPrevision) {
    //  return base64ChartPrevision.map((item, index) => {
    //   return <Base64Image key={index} base64={item["previsione_status"]} />
    // })
    }

  }

  return (
    <div>
      <section className="h-full gradient-form bg-blue-100 md:h-screen overflow-auto">
        <div className="container py-12 h-full">
          <div className="flex justify-center items-center flex-wrap h-full g-6 text-gray-800">
            <div className="xl:w-10/12">
              <div className="block bg-white shadow-lg rounded-lg">
                <div className="lg:flex lg:flex-wrap g-0">
                  <div className="ml-4 lg:w-6/12 px-4 md:px-0">
                    <div className="md:p-12 md:mx-6">
                      <div className="text-left">
                        <h3 className="text-xl font-semibold mt-2 pt-3 mb-0 pb-1">Apartment &quot;{state["apartment_name"]}&quot;</h3>

                        <h4 className="text-xl font-semibold mt-1 mb-0 pb-1">
                          Welcome in your house dashboard {state["firstname"]} {state["surname"]}.
                        </h4>
                        <h4 className="text-l font-semibold mt-1 mb-4 pb-1">Today is {weekday[new Date().getDay()]}, beautiful day, isn&apos;t it?</h4>
                      </div>
                    </div>

                    <h3 className="text-xl font-semibold mt-2 pt-3 mb-4 pb-1">Let me guess 🔮</h3>


                    <BinProphetRecord color={typologyColorMap[type].length === 0 ? typologyColorMap["other"] : typologyColorMap[type]} date="test" sort_type="test_tip" filling={parseFloat("0.95")} />
                    <BinProphetRecord color={typologyColorMap[type].length === 0 ? typologyColorMap["other"] : typologyColorMap[type]} date="test" sort_type="test_tip" filling={parseFloat("1.0")} />


                    <div className="mb-4 mt-16">Lorem, ipsum dolor sit amet consectetur adipisicing elit. Rerum qui quibusdam, beatae ipsum labore voluptatibus ratione, itaque expedita neque natus consequuntur et culpa voluptatem odit ipsam excepturi accusantium cum laudantium consequatur tenetur necessitatibus velit amet eum optio? Quaerat porro, officia obcaecati excepturi natus quo fugit perferendis eveniet laborum, quas nostrum.</div>

                    <div className="text-center pt-1 mb-12 pb-1">
                      <button
                        className="bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded"
                        onClick={handleToggle}
                      >
                        {isOpen ? <FaMinus /> : <FaPlus />}
                        {isOpen ? 'Hide' : 'Show'}
                      </button>
                      {/* <a className="text-gray-500" href="#!">Tutto apposto?</a>
                                            
*/}
                    </div>
                  </div>
                </div>
                <Collapse isOpened={isOpen}>
                  <div className={`transition-all duration-700 ${isOpen ? 'max-h-96 overflow-auto' : 'max-h-0'}`}>

                    <div className="lg:w-6/12 flex items-center lg:rounded-r-lg rounded-b-lg lg:rounded-bl-none">
                      <div className="text-black px-4 py-6 md:p-12 md:mx-6">
                        <h4 className="text-xl font-semibold mb-6">Prevision Charts:</h4>
                        <div className="">Check the actual filling forecast for each data-avialable typlogy for your apartment &hearts; </div>
                        <div className="my-6">
                    <span>ciao</span>

                        </div>
                      </div>
                    </div>
                  </div>
                </Collapse>
              </div>
            </div>
          </div>
        </div>
      </section >
    </div>
  );
};

export default Home;
