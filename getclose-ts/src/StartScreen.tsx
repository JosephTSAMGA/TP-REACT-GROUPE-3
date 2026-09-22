import "./StartScreen.css";

type StartScreenProps = {
  onStart?: () => void;
};

export default function StartScreen({ onStart = () => {} }: StartScreenProps) {
  return (
    <div className="start-screen">
      <div className="start-content">
        <p className="start-eyebrow">Jeu de géographie</p>
        <h1 className="start-title">GetClose</h1>
        <p className="start-tagline">
          Une photo, une carte, cinq manches. Devine où tu es, le plus près possible.
        </p>
        <button className="start-button" onClick={onStart}>
          Jouer
        </button>
      </div>
    </div>
  );
}