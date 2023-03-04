import React, { useState } from 'react';

export type Person = {
    name: string;
    surname: string;
    telegramUsername: string;
};

type Props = {
    onPeopleChange: (people: Person[]) => void;
};

const PersonList = (props: Props) => {
    const [name, setName] = useState('');
    const [surname, setSurname] = useState('');
    const [extension, setExtension] = useState(0);
    const [telegramUsername, setTelegramUsername] = useState('');
    const [people, setPeople] = useState<Person[]>([]);

    const addPerson = () => {
        const newPerson: Person = {
            name,
            surname,
            telegramUsername,
        };
        const newPeople = [...people, newPerson];
        setPeople(newPeople);
        if (props.onPeopleChange) {
            props.onPeopleChange(newPeople);
        }
        setName('');
        setSurname('');
        setExtension(0);
        setTelegramUsername('');
    };

    const removePerson = (index: number) => {
        const newPeople = [...people];
        newPeople.splice(index, 1);
        setPeople(newPeople);
        if (props.onPeopleChange) {
            props.onPeopleChange(newPeople);
        }
    };

    return (
        <div className='ml-4'>
            <div className='mb-2'>
                <h2>Insert data of <span className='font-bold'>{people.length + 1}º</span> co-occupant:</h2>
            </div>
            <div>
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Name:
                    <input
                        type="text"
                        className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </label>
                <br />
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Surname:
                    <input
                        type="text"
                        value={surname}
                        className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                        onChange={(e) => setSurname(e.target.value)}
                    />
                </label>
                <br />
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Extension:
                    <input
                        className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                        type="number"
                        value={extension}
                        onChange={(e) => setExtension(parseInt(e.target.value))}
                    />
                </label>
                <br />
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Telegram Username:
                    <input
                        type="text"
                        className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                        value={telegramUsername}
                        onChange={(e) => setTelegramUsername(e.target.value)}
                    />
                </label>
                <br />
                <button onClick={addPerson}>Add Person</button>
            </div>
            <ul>
                {people.map((person, index) => (
                    <li key={index}>
                        {person.name} {person.surname} () @{person.telegramUsername}
                        <button onClick={() => removePerson(index)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PersonList;
