const logger = require('../logger'); // eslint-disable-line no-unused-vars

const bcrypt = require('bcrypt');
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class User extends Model {
    static async createSecure({
      email,
      password,
    }) {
      const salt = await bcrypt.genSalt(12);
      return User.create({
        email: email.trim().toLowerCase(),
        password: await bcrypt.hash(password, salt),
      });
    }

    static isPasswordShort(password) {
      return password.length < 12;
    }

    async checkPassword(password) {
      return bcrypt.compare(password, this.password);
    }
  }

  User.init({
    email: DataTypes.STRING,
    password: DataTypes.STRING,
    admin: DataTypes.BOOLEAN,
  }, {
    sequelize,
    modelName: 'User',
    tableName: 'users',
    createdAt: 'created_at',
    updatedAt: 'updated_at',
    deletedAt: 'deleted_at',
    paranoid: true,
  });

  return User;
};
