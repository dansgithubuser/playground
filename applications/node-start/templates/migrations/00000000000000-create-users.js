module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('users', {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true,
      },
      email: {
        allowNull: false,
        type: Sequelize.STRING,
      },
      password: {
        allowNull: false,
        type: Sequelize.STRING,
      },
      admin: Sequelize.BOOLEAN,
      created_at: {
        allowNull: false,
        type: Sequelize.DATE,
      },
      updated_at: {
        allowNull: false,
        type: Sequelize.DATE,
      },
      deleted_at: Sequelize.DATE,
    });
    await queryInterface.addIndex('users', ['email']);
  },
  down: async (queryInterface, Sequelize) => { // eslint-disable-line no-unused-vars
    await queryInterface.dropTable('users');
  },
};
