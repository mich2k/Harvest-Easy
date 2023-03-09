import React from 'react';

interface Props {
  base64: string;
}

const Base64Image: React.FC<Props> = ({ base64 }) => {
  const src = `data:image/jpeg;base64,${base64}`;
  return <img src={src} alt="base64 image" />;
};

export default Base64Image;
