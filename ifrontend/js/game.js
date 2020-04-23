const width = 600;
const height = 480;
const speed = 110;

const config = {
    type: Phaser.WEBGL,
    width: width,
    height: height,
    scene: {
        preload: preload,
        create: create,
        update: update
    },
    physics: {
        default: 'arcade',
        arcade: {
            //gravity: { y: 300 },
            debug: false
        }
    },
    pixelArt: true,
    zoom: 1
};

const tilesize = 16;
let offsetX = 0;
let offsetY = 0;

var game = new Phaser.Game(config);

var chr = {
    helth: 100,
    x: height/2,
    y: width/2,
}

var tree = {
    key: 'Tree1',
    x: height/3,
    y: width/3
}
var trees;
var player;
var helthText;
function treeDamage(player, tree){
    console.log("tree damage")
    console.log(player)
    chr.helth -= 1;
    helthText.setText('helth: '+chr.helth)
}
function preload() {
    this.load.image('Grass', 'assets/Grass.png');
    this.load.image('Tree1', 'assets/Tree1.png');
    this.load.image('Tree2', 'assets/Tree2.png');
    this.load.image('Tree3', 'assets/Tree3.png');
    this.load.image('Sea', 'assets/Sea.png');
    this.load.image('Boat1', 'assets/Boat1.png');
    this.load.image('Boat2', 'assets/Boat2.png');
    this.load.image('Sand', 'assets/Sand.png');
    this.load.image('character', 'assets/character/tile000.png')
    noise.seed(Math.random());
    cursors = this.input.keyboard.createCursorKeys();
}

function create() {
    //scene.add.displayList.removeAll();
    for (let y = 0; y < (height / tilesize); y++) {
        for (let x = 0; x < (width / tilesize); x++) {
            let posX = (x * tilesize) + 8;
            let posY = (y * tilesize) + 8;
                this.make.image({
                    x: posX,
                    y: posY,
                    key: 'Grass',
                    add: true
                });
        }
    }
    helthText = this.add.text(16, 16, 'helth: '+chr.helth, { fontSize: '32px', fill: '#000' });
    trees = this.physics.add.staticGroup();
    trees.create(tree.x, tree.y, tree.key);
    
    player = this.physics.add.sprite(chr.x, chr.y, 'character')
    player.setCollideWorldBounds(true);
    player.setBounce
    //this.physics.add.collider(player, trees);
    this.physics.add.collider(player, trees, treeDamage, null, this);
    draw(this);
}

function update() {
    if (cursors.left.isDown) { player.setVelocityX(-speed) }
    else if (cursors.right.isDown) { player.setVelocityX(speed) }
    else if (cursors.up.isDown) { player.setVelocityY(-speed) }
    else if (cursors.down.isDown) { player.setVelocityY(speed); }
    else {player.setVelocityX(0); player.setVelocityY(0)}
    draw(this);
}

function draw(scene) {
    //scene.add.tileSprite(height/2, width/2, 32, 32, 'character')
    // scene.add.image(tree.x, tree.y, tree.key);
}

function between(value1, value2, value3) {
    return (value2 < value1 && value1 < value3)
}