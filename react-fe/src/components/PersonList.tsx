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
    <div>
      <h2>Person List</h2>
      <div>
        <label>
          Name:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>
        <br />
        <label>
          Surname:
          <input
            type="text"
            value={surname}
            onChange={(e) => setSurname(e.target.value)}
          />
        </label>
        <br />
        <label>
          Extension:
          <input
            type="number"
            value={extension}
            onChange={(e) => setExtension(parseInt(e.target.value))}
          />
        </label>
        <br />
        <label>
          Telegram Username:
          <input
            type="text"
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
