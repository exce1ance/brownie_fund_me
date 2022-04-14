from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    print(f"La cuenta es: {account}")

    # pass the price feed address to out fundme contract

    # if we are on a persistent network like rinkeby, use associated address "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e"
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # .get("verify") se puede reemplazar por ["verify"] pero si te olvidas de ponerlo en config, con esto lo verifica solo
    # # publish_source es para que verifique el contrato una vez hecho el deploy (Para version de comp 0.8.4 hay algo medio tricky.. ojo)
    print(f"Contract deployed to {fund_me.address}")
    return fund_me  # para usar en el testing


def main():
    deploy_fund_me()
