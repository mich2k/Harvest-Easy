

export default function handler(req, res) {
  const { apartment_id } = req.query;
  //some other codes...
  res.status(200).json({ apartment_id });
}