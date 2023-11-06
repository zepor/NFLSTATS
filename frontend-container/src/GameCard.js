function GameCard({ game }) {
    return (
        <div className="card mb-4">
            <h5 className="card-header">
                {game.awayteam.name} ({game.awayteam.alias}) VS 
                {game.hometeam.name} ({game.hometeam.alias})
            </h5>
            <div className="card-body">
                <p>Broadcast: {game.broadcast.network}</p>
                <p>Game Type: {game.gamegame.game_type}</p>
                <p>Scheduled Time: {new Date(game.gamegame.scheduled).toLocaleTimeString()}</p>
                <p>Status: {game.gamegame.status}</p>
                {/* Add more details as needed */}
            </div>
        </div>
    );
}
